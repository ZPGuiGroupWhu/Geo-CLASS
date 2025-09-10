# 利用大模型GPT3.5运行后续任务（即与语料库内容进行映射），此处为部分剪枝后GCMD.json中前四层内容（token限制）
import os
import json
import pandas as pd
import openai
from dotenv import load_dotenv, find_dotenv

# 加载环境变量
_ = load_dotenv(find_dotenv())

# 代理配置
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7890'

# 获取API密钥
openai.api_key = os.environ['OPENAI_API_KEY']

# 递归函数来提取所有的键
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


# 加载函数词典
Function_path = r'.\00 Corpus\GCMD.json'
with open(Function_path, 'r', encoding='utf-8') as f:
    Function_data = json.load(f)
Function_corpus = []
extract_keys(Function_data, Function_corpus, max_depth=4)
print(len(Function_corpus))

# 读取CSV文件
csv_path = r'.\Data\GPT3.5\theme_sample.csv'
df = pd.read_csv(csv_path)


# 确保新增的列存在，并将其数据类型设置为字符串类型
if 'GPT3.5' not in df.columns:
    df['GPT3.5'] = ""
if 'Usage' not in df.columns:
    df['Usage'] = ""


# 定义API调用函数
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
SURFACE MASS
GASES
GROUND WATER
METALS
OCEAN WAVES
"""

# 固定的提示信息
fixed_prompt = f'Your role: Technical assistant proficient in document analysis\n\n' + \
               f'Your task: Determine which item from the following list best matches the given input: {Function_corpus}\n\n' + \
               f'Your requirement: Just select the best matching element from the corpus for each Input\n\n' + \
               f'Output the matched concept results line by line in order, without additional symbols (such as "-", etc.) and additional explanations, and without blank lines between results\n\n'+ \
               f'Your reply example: {output_example} \n\n'

batch_size = 5
total_rows = len(df)
num_batches = (total_rows + batch_size - 1) // batch_size  # 计算总批次

# 按批次处理数据
for batch_num in range(num_batches):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, total_rows)
    batch_prompts = []
    for index in range(start_idx, end_idx):
        function_value = df.at[index, 'Value']
        batch_prompts.append(f'Input: {function_value}')
    print("Input: ", batch_prompts)

    # 处理批次数据
    combined_prompt = fixed_prompt + "\n\n".join(batch_prompts)
    response, token_usage = get_completion(combined_prompt)
    print("Output: ", response)

    # 处理返回结果，假设每个结果按顺序分行
    response_lines = response.split('\n')

    for i, line in enumerate(response_lines):
        if start_idx + i < end_idx:
            if line.strip():  # 检查结果行是否为空
                df.at[start_idx + i, 'GPT3.5'] = line.strip()
                df.at[start_idx + i, 'Usage'] = token_usage

    # 每处理10个批次后保存并暂停
    if (batch_num + 1) % 100 == 0:
        df.to_csv(csv_path, index=False)
        print(f"Processed {batch_num + 1} batches. Check the CSV file for results.")
        user_input = input("Do you want to continue processing the next 10 batches? (yes/no): ")
        if user_input.lower() != 'yes':
            break

# 保存最终结果
df.to_csv(csv_path, index=False)
