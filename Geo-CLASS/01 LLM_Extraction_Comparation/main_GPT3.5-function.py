# Use the large model GPT3.5 to run subsequent tasks (i.e., map with the corpus content). Here is all the contents in Function_Dictionary.txt (no token restrictions)
import os
import json
import pandas as pd
import openai
from dotenv import load_dotenv, find_dotenv

# Loading environment variables
_ = load_dotenv(find_dotenv())

# Proxy Configuration
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7890'

# Get an API key
openai.api_key = os.environ['OPENAI_API_KEY']


# Recursive function to extract all keys
def extract_keys(data, keys_list, depth=1, max_depth=None):
    if max_depth is not None and depth > max_depth:
        return

    if isinstance(data, dict):
        for key, value in data.items():
            keys_list.append(key)
            extract_keys(value, keys_list, depth + 1, max_depth)
    elif isinstance(data, list):
        for item in data:
            extract_keys(item, keys_list, depth + 1, max_depth)


# Loading function dictionary
Function_path = r'./00 Corpus/Function_Dictionary.txt'
with open(Function_path, 'r', encoding='utf-8') as f:
    Function_data = json.load(f)
Function_corpus = []
extract_keys(Function_data, Function_corpus)
print(len(Function_corpus))

# Reading CSV Files
csv_path = r'./Data/GPT3.5/function_sample.csv'
df = pd.read_csv(csv_path)


# Make sure the new column exists and set its data type to string.
if 'GPT3.5' not in df.columns:
    df['GPT3.5'] = ""
if 'Usage' not in df.columns:
    df['Usage'] = ""


# Define API call function
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.2, messages=None):
    if messages is None:
        messages = []

    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    response_content = response.choices[0].message["content"]
    token_usage = response.usage['total_tokens']
    messages.append({"role": "system", "content": response_content})
    return response_content, token_usage


output_example = r"""
Select Specific Polarization From Images
Filter And Mosaic Landsat Images
Calculate Temporal Spectral Indices
Calculate Difference Normalized Burn Ratio (dNBR)
Export Processed Images To Drive
"""

# Fixed prompt information
fixed_prompt = f'Your role: Technical assistant proficient in document analysis\n\n' + \
               f'Your task: Determine which item from the following list best matches the given input: {Function_corpus}\n\n' + \
               f'Your requirement: Just select the best matching element from the corpus for each Input\n\n' + \
               f'Output the matched concept results line by line in order, without additional symbols (such as "-", etc.) and additional explanations, and without blank lines between results\n\n'+ \
               f'Your reply example: {output_example} \n\n'

batch_size = 5
total_rows = len(df)
num_batches = (total_rows + batch_size - 1) // batch_size  # Calculate the total batch size

# Process data in batches
for batch_num in range(num_batches):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, total_rows)
    batch_prompts = []
    for index in range(start_idx, end_idx):
        function_value = df.at[index, 'Value']
        batch_prompts.append(f'Input: {function_value}')
    print("Input: ", batch_prompts)

    # Processing batch data
    combined_prompt = fixed_prompt + "\n\n".join(batch_prompts)
    response, token_usage = get_completion(combined_prompt)
    print("Output: ", response)

    # Process the returned results, assuming that each result is separated into rows in sequence
    response_lines = response.split('\n')

    for i, line in enumerate(response_lines):
        if start_idx + i < end_idx:
            if line.strip():  # Check if the result row is empty
                df.at[start_idx + i, 'GPT3.5'] = line.strip()
                df.at[start_idx + i, 'Usage'] = token_usage

    # Save and pause after processing every 10 batches
    if (batch_num + 1) % 200 == 0:
        df.to_csv(csv_path, index=False)
        print(f"Processed {batch_num + 1} batches. Check the CSV file for results.")
        user_input = input("Do you want to continue processing the next 10 batches? (yes/no): ")
        if user_input.lower() != 'yes':
            break

# Save the final result
df.to_csv(csv_path, index=False)
