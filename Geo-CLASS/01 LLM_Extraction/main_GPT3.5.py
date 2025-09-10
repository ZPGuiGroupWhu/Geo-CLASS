# 用openAI的方式调用GPT系列模型
import os
import openai
import Extractor_Constant
from dotenv import load_dotenv, find_dotenv
from Script_preprocessing import read_and_clean_file

# find_dotenv()寻找并定位.env文件的路径
# load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中
# 如果你设置的是全局的环境变量，这行代码则没有任何作用。
_ = load_dotenv(find_dotenv())

# 如果你需要通过代理端口访问，你需要如下配置
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7890'

# 获取环境变量 OPENAI_API_KEY
openai.api_key = os.environ['OPENAI_API_KEY']

input_folder = r".\GEE_Samples"
output_folder = r".\LLM_Extraction_Result\GPT_3.5"

# 检查输出文件夹是否存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

Entity_role = Extractor_Constant.Entity_role
Entity_task = Extractor_Constant.Entity_task
Entity_requirement_str = Extractor_Constant.Entity_requirement_str
Entity_reply_example = Extractor_Constant.Entity_reply_example

Relation_role = Extractor_Constant.Relation_role
Relation_task = Extractor_Constant.Relation_task
Relation_requirement_str = Extractor_Constant.Relation_requirement_str
Relation_reply_example = Extractor_Constant.Relation_reply_example


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.2, messages=None):
    '''
    Retrieve completions from the OpenAI API, preserving conversation history.
    '''
    if messages is None:
        messages = []

    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    response_content = response.choices[0].message["content"]
    messages.append({"role": "system", "content": response_content})
    return response_content, messages


# 获取两个文件夹中的文件名
sample_files = set(os.listdir(input_folder))
result_files = set(os.listdir(output_folder))

# 找出只在sample_dir中存在的文件
files_to_process = sample_files - result_files
print(files_to_process)

# 处理这些文件
for file_name in files_to_process:
    if file_name.endswith('.txt'):
        file_path = os.path.join(input_folder, file_name)
        GEE_script = read_and_clean_file(file_path)

        Entity_prompt = f'Your role: {Entity_role} \n\n' + \
                        f'Your task: {Entity_task} \n {GEE_script} \n\n' + \
                        f'Your reply needs to meet these requirements: \n {Entity_requirement_str} \n\n' + \
                        f'Your reply example: {Entity_reply_example} \n\n'

        entity, history = get_completion(Entity_prompt)
        print(entity)

        Relation_prompt = f'Your role: {Relation_role} \n\n' + \
                          f'Your task: {Relation_task} \n {entity}\n\n' + \
                          f'Your reply needs to meet these requirements: \n {Relation_requirement_str} \n\n' + \
                          f'Your reply example: {Relation_reply_example} \n\n'
        relation, history = get_completion(Relation_prompt, messages=history)
        print(relation)
        output_file_path = os.path.join(output_folder, os.path.basename(file_path))
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Entity Recognition:\n{entity}\n\nRelation Extraction:\n{relation}")

