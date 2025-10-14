# Use the Qianfan model to call Meta-Llama-3-70B to run subsequent tasks (i.e., map with the corpus content). Here is the first 5 layers of content in the entire Function_Dictionary.txt (token limit)
import os
import json
import pandas as pd
import qianfan


# Recursive function to extract all keys
def extract_keys(data, keys_list, depth=1, max_depth=None):
    # Checks whether the user-specified maximum depth has been reached
    if max_depth is not None and depth > max_depth:
        return

    if isinstance(data, dict):
        for key, value in data.items():
            keys_list.append(key)
            extract_keys(value, keys_list, depth + 1, max_depth)
    elif isinstance(data, list):
        for item in data:
            extract_keys(item, keys_list, depth + 1, max_depth)


Function_path = r'./00 Corpus/Function_Dictionary.txt'  # Input file path
with open(Function_path, 'r', encoding='utf-8') as f:
    Function_data = json.load(f)
Function_corpus = []
extract_keys(Function_data, Function_corpus, max_depth=5)
print(len(Function_corpus))
# print(GCMD_corpus)

# Reading CSV Files
csv_path = r'./Data/LLAMA70B/function_sample.csv'
df = pd.read_csv(csv_path)

# Make sure the newly added column exists
if 'LLAMA70B' not in df.columns:
    df['LLAMA70B'] = ""
if 'Usage' not in df.columns:
    df['Usage'] = ""


# Set authentication information
os.environ["QIANFAN_ACCESS_KEY"] = YOUR_QIANFAN_ACCESS_KEY
os.environ["QIANFAN_SECRET_KEY"] = YOUR_QIANFAN_SECRET_KEY

chat_comp = qianfan.ChatCompletion()


# # Input topic corpus
# theme_corpus_prompt = f'Your role: {Extractor_Constant_LLAMA.Corpus_role} \n\n' + \
#                       f'Your task: {Extractor_Constant_LLAMA.Corpus_task1} \n {GCMD_corpus} \n\n'
# resp = chat_comp.do(model="Meta-Llama-3-70B", messages=[{
#     "role": "user",
#     "content": theme_corpus_prompt
# }], temperature=0.2)
# theme_corpus_content = resp["body"]
# # corpus = corpus_content['result']
# theme_corpus_usage = theme_corpus_content['usage']
# print(theme_corpus_usage)

# Update CSV file
for index, row in df.iterrows():
    function_value = row['Value']
    function_corpus_prompt = f'Your role: Technical assistant proficient in document analysis\n\n' + \
                          f'Your task: Determine which theme from the following list best matches the given input: {Function_corpus}\n\n' + \
                          f'Your requirement: Just select the best element from the corpus for output, no additional explanation is needed\n\n' + \
                          f'Input: {function_value}\n\n'

    # Calling the LLLM
    response = chat_comp.do(model="Meta-Llama-3-70B", messages=[{
        "role": "user",
        "content": function_corpus_prompt
    }], temperature=0.2)

    # Assume that the returned result is the most similar topic
    function_corpus_content = response["body"]
    most_similar_function = function_corpus_content['result']  # Adjust according to the actual return structure
    function_corpus_usage = function_corpus_content['usage']
    print(function_corpus_usage)

    # Update DataFrame
    df.at[index, 'Value_LLAMA70B'] = most_similar_function
    df.at[index, 'Usage'] = function_corpus_usage

# Save the updated CSV
df.to_csv(csv_path, index=False)

