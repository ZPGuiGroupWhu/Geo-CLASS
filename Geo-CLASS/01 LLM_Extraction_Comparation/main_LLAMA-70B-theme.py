# 利用千帆大模型调用Meta-Llama-3-70B运行后续任务（即与语料库内容进行映射），此处为部分剪枝后GCMD.json中前四层内容（token限制）
import os
import json
import pandas as pd
import qianfan


# 递归函数来提取所有的键
def extract_keys(data, keys_list, depth=1, max_depth=None):
    # 检查是否达到了用户指定的最大深度
    if max_depth is not None and depth > max_depth:
        return

    if isinstance(data, dict):
        for key, value in data.items():
            keys_list.append(key)
            extract_keys(value, keys_list, depth + 1, max_depth)
    elif isinstance(data, list):
        for item in data:
            extract_keys(item, keys_list, depth + 1, max_depth)


GCMD_path = r'.\00 Corpus\GCMD.json'  # 输入文件路径
with open(GCMD_path, 'r', encoding='utf-8') as f:
    GCMD_data = json.load(f)
GCMD_corpus = []
extract_keys(GCMD_data, GCMD_corpus, max_depth=4)
print(len(GCMD_corpus))
# print(GCMD_corpus)

# 读取CSV文件
csv_path = r'.\Data\LLAMA70B\theme_sample.csv'
df = pd.read_csv(csv_path)

# 确保新增的列存在
if 'LLAMA70B' not in df.columns:
    df['LLAMA70B'] = ""
if 'Usage' not in df.columns:
    df['Usage'] = ""


# 设置认证信息
os.environ["QIANFAN_ACCESS_KEY"] = YOUR_QIANFAN_ACCESS_KEY
os.environ["QIANFAN_SECRET_KEY"] = YOUR_QIANFAN_SECRET_KEY

chat_comp = qianfan.ChatCompletion()

# 更新CSV文件
for index, row in df.iterrows():
    theme_value = row['Value']
    theme_corpus_prompt = f'Your role: Technical assistant proficient in document analysis\n\n' + \
                          f'Your task: Determine which theme from the following list best matches the given input: {GCMD_corpus}\n\n' + \
                          f'Your requirement: Just select the best element from the corpus for output, no additional explanation is needed\n\n' + \
                          f'Input: {theme_value}\n\n'

    # 调用大模型
    response = chat_comp.do(model="Meta-Llama-3-70B", messages=[{
        "role": "user",
        "content": theme_corpus_prompt
    }], temperature=0.2)

    # 假设返回结果是最相似的主题
    theme_corpus_content = response["body"]
    most_similar_theme = theme_corpus_content['result']  # 根据实际的返回结构调整
    theme_corpus_usage = theme_corpus_content['usage']
    print(theme_corpus_usage)

    # 更新DataFrame
    df.at[index, 'Value_LLAMA70B'] = most_similar_theme
    df.at[index, 'Usage'] = theme_corpus_usage

# 保存更新后的CSV
df.to_csv(csv_path, index=False)