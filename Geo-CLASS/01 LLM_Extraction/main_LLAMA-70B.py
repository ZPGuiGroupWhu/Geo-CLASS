# 用千帆大模型的方式调用Meta-Llama-3-70B
import os
import qianfan
import Extractor_Constant
from Script_preprocessing import read_and_clean_file

# 设置认证信息
os.environ["QIANFAN_ACCESS_KEY"] = "BAIDU_API_KEY"
os.environ["QIANFAN_SECRET_KEY"] = "BAIDU_SECRET_KEY"

chat_comp = qianfan.ChatCompletion()

input_folder = r".\GEE_Samples"
output_folder = r".\LLM_Extraction_Result\LLAMA70B"

# 检查输出文件夹是否存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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

        Entity_prompt = f'Your role: {Extractor_Constant.Entity_role} \n\n' + \
                        f'Your task: {Extractor_Constant.Entity_task} \n {GEE_script} \n\n' + \
                        f'Your reply needs to meet these requirements: \n {Extractor_Constant.Entity_requirement_str} \n\n' + \
                        f'Your reply example: {Extractor_Constant.Entity_reply_example} \n\n'

        if len(Entity_prompt) > 20000:
            print(f"Error: Input text exceeds maximum limit of 20000 characters. Skipping file {file_name}")
            continue

        resp = chat_comp.do(model="Meta-Llama-3-70B", messages=[{
            "role": "user",
            "content": Entity_prompt
        }], temperature=0.2)
        entity_content = resp["body"]
        entity = entity_content['result']
        entity_usage = entity_content['usage']

        print(entity)

        Relation_prompt = f'Your role: {Extractor_Constant.Relation_role} \n\n' + \
                          f'Your task: {Extractor_Constant.Relation_task} \n {entity}\n\n' + \
                          f'Your reply needs to meet these requirements: \n {Extractor_Constant.Relation_requirement_str} \n\n' + \
                          f'Your reply example: {Extractor_Constant.Relation_reply_example} \n\n'

        resp = chat_comp.do(model="Meta-Llama-3-70B", messages=[{
            "role": "user",
            "content": Relation_prompt
        }], temperature=0.2)
        relation_content = resp["body"]
        relation = relation_content['result']
        relation_usage = relation_content['usage']

        print(relation)

        total_prompt_tokens = entity_usage['prompt_tokens'] + relation_usage['prompt_tokens']
        total_completion_tokens = entity_usage['completion_tokens'] + relation_usage['completion_tokens']
        total_tokens = entity_usage['total_tokens'] + relation_usage['total_tokens']

        total_usage = {
            'prompt_tokens': total_prompt_tokens,
            'completion_tokens': total_completion_tokens,
            'total_tokens': total_tokens
        }

        output_file_path = os.path.join(output_folder, os.path.basename(file_path))
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Entity Recognition:\n{entity}\n\nRelation Extraction:\n{relation}\n\nTotal_Usage:\n{total_usage}")