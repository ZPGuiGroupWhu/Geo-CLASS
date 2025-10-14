# Use the Qianfan model to call Meta-Llama-3-70B to run subsequent tasks (i.e., map with the corpus content). Here are the first four layers of content in GCMD.json after partial pruning (token restriction)
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


GCMD_path = r'.\00 Corpus\GCMD.json'  # Input file path
with open(GCMD_path, 'r', encoding='utf-8') as f:
    GCMD_data = json.load(f)
GCMD_corpus = []
extract_keys(GCMD_data, GCMD_corpus, max_depth=4)
print(len(GCMD_corpus))
# print(GCMD_corpus)

# Reading CSV Files
csv_path = r'.\Data\LLAMA70B\theme_sample.csv'
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

# Update CSV file
for index, row in df.iterrows():
    theme_value = row['Value']
    theme_corpus_prompt = f'Your role: Technical assistant proficient in document analysis\n\n' + \
                          f'Your task: Determine which theme from the following list best matches the given input: {GCMD_corpus}\n\n' + \
                          f'Your requirement: Just select the best element from the corpus for output, no additional explanation is needed\n\n' + \
                          f'Input: {theme_value}\n\n'

    # Calling the large model
    response = chat_comp.do(model="Meta-Llama-3-70B", messages=[{
        "role": "user",
        "content": theme_corpus_prompt
    }], temperature=0.2)

    # Assume that the returned result is the most similar topic
    theme_corpus_content = response["body"]
    most_similar_theme = theme_corpus_content['result']  # Adjust according to the actual return structure
    theme_corpus_usage = theme_corpus_content['usage']
    print(theme_corpus_usage)

    # Update DataFrame
    df.at[index, 'Value_LLAMA70B'] = most_similar_theme
    df.at[index, 'Usage'] = theme_corpus_usage

# Save the updated CSV
df.to_csv(csv_path, index=False)
