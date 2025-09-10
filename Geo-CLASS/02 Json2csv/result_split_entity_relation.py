# 把结果文件处理成两个部分的文件，分别为Entity和Relation

# 常规结果：两部分'''json '''的操作
import os
import re

# 指定输入文件夹路径
input_folder = r"F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE"

# 指定输出文件夹路径
output_folder_entity = r"F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE\Entity"
output_folder_relation = r"F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE\Relation"
error_log_path = r"F:\GEE\GEE量化样本01\Experiment\sample_241_ERNIE\err.txt"

# 如果输出文件夹不存在，就创建它们
os.makedirs(output_folder_entity, exist_ok=True)
os.makedirs(output_folder_relation, exist_ok=True)

# # 正则表达式模式，用于查找 JSON 块的起始位置
# json_start_pattern = re.compile(r'({)', re.DOTALL)

# 错误计数和错误信息列表
error_count = 0
error_messages = []


def find_json_blocks(content):
    """从内容中找到所有的 JSON 块"""
    brace_count = 0
    in_string = False
    escaped = False
    blocks = []
    current_block = []
    start_index = -1

    for i, char in enumerate(content):
        if char == '"' and not escaped:
            in_string = not in_string
        if not in_string:
            if char == '{':
                if brace_count == 0:
                    start_index = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    blocks.append(content[start_index:i + 1])
                    start_index = -1

        current_block.append(char)
        if char == '\\' and not escaped:
            escaped = True
        else:
            escaped = False

    return blocks

# 遍历输入文件夹中的每一个文件
for filename in os.listdir(input_folder):
    # 生成完整的文件路径
    filepath = os.path.join(input_folder, filename)

    # 确保路径指向的是一个文件，而不是一个文件夹
    if os.path.isfile(filepath):
        # 读取文件内容
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

            # 找到所有 JSON 块
            json_blocks = find_json_blocks(content)
            entity_found = False
            relation_found = False

            # 处理每个 JSON 块
            for block in json_blocks:
                if '"Theme"' in block:
                    with open(os.path.join(output_folder_entity, filename.replace(".txt", ".txt")), 'w',
                              encoding='utf-8') as file:
                        # file.write(block)
                        file.write(block.strip())
                    entity_found = True

                if any(key in block for key in ['"relation_1"', '"Relation_1"', '"relationship_1","relation_1"']):
                    with open(os.path.join(output_folder_relation, filename.replace(".txt", ".txt")), 'w',
                              encoding='utf-8') as file:
                        # file.write(block)
                        file.write(block.strip())
                    relation_found = True

            if not entity_found:
                error_count += 1
                error_messages.append(f"File {filename} does not contain 'Theme' content.")

            if not relation_found:
                error_count += 1
                error_messages.append(
                    f"File {filename} does not contain 'relation_1', 'Relation_1' or 'relationship_1' content.")

    # 将错误信息写入 err.txt 文件
    with open(error_log_path, 'w', encoding='utf-8') as error_file:
        for message in error_messages:
            error_file.write(message + '\n')

    print(f"Total errors: {error_count}")
    print(f"Error details saved to {error_log_path}")



# # 不常规结果：关系实体分别在两部分'''json '''的情况也有，关系实体在同一个'''json '''的情况也有
# import os
# import re
# import json
#
# # 指定输入文件夹路径
# input_folder = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoE"
#
# # 指定输出文件夹路径
# output_folder_entity = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoE\Entity"
# output_folder_relation = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoE\Relation"
# error_log_path = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoE\err.txt"
#
# # 如果输出文件夹不存在，就创建它们
# os.makedirs(output_folder_entity, exist_ok=True)
# os.makedirs(output_folder_relation, exist_ok=True)
#
# # 错误计数和错误信息列表
# error_count = 0
# error_messages = []
#
# def extract_json_blocks(content):
#     """从内容中提取所有的 JSON 块"""
#     pattern = re.compile(r'```json\n(.*?)\n```', re.DOTALL)
#     return pattern.findall(content)
#
# # 遍历输入文件夹中的每一个文件
# for filename in os.listdir(input_folder):
#     # 生成完整的文件路径
#     filepath = os.path.join(input_folder, filename)
#
#     # 确保路径指向的是一个文件，而不是一个文件夹
#     if os.path.isfile(filepath):
#         # 读取文件内容
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()
#
#             # 提取所有的 JSON 块
#             json_blocks = extract_json_blocks(content)
#
#             for block in json_blocks:
#                 json_data = json.loads(block)
#
#                 # 处理实体部分
#                 if "Theme" in json_data:
#                     with open(os.path.join(output_folder_entity, filename.replace(".txt", ".txt")), 'w', encoding='utf-8') as file:
#                         file.write(json.dumps(json_data, ensure_ascii=False, indent=4))
#
#                 # 处理关系部分
#                 if any(key.startswith("relation_") for key in json_data):
#                     with open(os.path.join(output_folder_relation, filename.replace(".txt", ".txt")), 'w', encoding='utf-8') as file:
#                         file.write(json.dumps(json_data, ensure_ascii=False, indent=4))
#
# # 将错误信息写入 err.txt 文件
# with open(error_log_path, 'w', encoding='utf-8') as error_file:
#     for message in error_messages:
#         error_file.write(message + '\n')
#
# print(f"Total errors: {error_count}")
# print(f"Error details saved to {error_log_path}")


# # 不常规结果：关系实体分别在两部分'''json '''的情况也有，关系实体在同一个'''json '''的情况也有，还有情况是实体没有'''json '''
# import os
# import re
# import json
#
# # 指定输入文件夹路径
# input_folder = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoR"
#
# # 指定输出文件夹路径
# output_folder_entity = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoR\Entity"
# output_folder_relation = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoR\Relation"
# error_log_path = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoR\err.txt"
#
# # 如果输出文件夹不存在，就创建它们
# os.makedirs(output_folder_entity, exist_ok=True)
# os.makedirs(output_folder_relation, exist_ok=True)
#
# # 错误计数和错误信息列表
# error_count = 0
# error_messages = []
#
# def extract_json_blocks(content):
#     """从内容中提取所有的 JSON 块"""
#     pattern = re.compile(r'```(?:json)?(.*?)```', re.DOTALL)
#     return pattern.findall(content)
#
# # 遍历输入文件夹中的每一个文件
# for filename in os.listdir(input_folder):
#     # 生成完整的文件路径
#     filepath = os.path.join(input_folder, filename)
#
#     # 确保路径指向的是一个文件，而不是一个文件夹
#     if os.path.isfile(filepath):
#         # 读取文件内容
#         with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
#             content = file.read()
#
#             # 提取所有的 JSON 块
#             json_blocks = extract_json_blocks(content)
#
#             for block in json_blocks:
#                 try:
#                     json_data = json.loads(block)
#                 except json.JSONDecodeError as e:
#                     error_count += 1
#                     error_messages.append(f"Error in file {filename}: {str(e)}")
#                     continue
#
#                 # 处理实体部分
#                 if any(key.startswith("Theme") for key in json_data) or "Entity Recognition" in json_data:
#                     entity_data = json_data if any(key.startswith("Theme") for key in json_data) else json_data.get("Entity Recognition")
#                     with open(os.path.join(output_folder_entity, filename.replace(".txt", ".txt")), 'a', encoding='utf-8') as file:
#                         file.write(json.dumps(entity_data, ensure_ascii=False, indent=4))
#                         file.write('\n')
#
#                 # 处理关系部分
#                 if any(key.startswith("relation_") for key in json_data) or "Relation Extraction" in json_data:
#                     relation_data = json_data if any(key.startswith("relation_") for key in json_data) else json_data.get("Relation Extraction")
#                     with open(os.path.join(output_folder_relation, filename.replace(".txt", ".txt")), 'a', encoding='utf-8') as file:
#                         file.write(json.dumps(relation_data, ensure_ascii=False, indent=4))
#                         file.write('\n')
#
# # 将错误信息写入 err.txt 文件
# with open(error_log_path, 'w', encoding='utf-8') as error_file:
#     for message in error_messages:
#         error_file.write(message + '\n')
#
# print(f"Total errors: {error_count}")
# print(f"Error details saved to {error_log_path}")


# # 看所有文件和split后的文件相差的文件
# import os
#
# input_folder = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoE"
# output_folder = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoE\Relation"
#
# # 检查输出文件夹是否存在，如果不存在则创建
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)
#
# # 获取两个文件夹中的文件名
# sample_files = set(os.listdir(input_folder))
# result_files = set(os.listdir(output_folder))
#
# # 找出只在sample_dir中存在的文件
# files_to_process = sample_files - result_files
# print(files_to_process)


# # 把"Entity Recognition:" { }开头的文件加上```json ```
# import os
#
# # 指定输入文件夹路径
# input_folder = r"F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B_Schema_NoR2"
#
# # 遍历输入文件夹中的每一个文件
# for filename in os.listdir(input_folder):
#     # 生成完整的文件路径
#     filepath = os.path.join(input_folder, filename)
#
#     # 确保路径指向的是一个文件，而不是一个文件夹
#     if os.path.isfile(filepath):
#         # 读取文件内容
#         with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
#             content = file.readlines()
#
#         # 检查并修改文件内容
#         new_content = []
#         inside_entity_recognition = False
#         for line in content:
#             if line.strip() == "Entity Recognition:":
#                 # 检查下一行是否是 {
#                 next_line_index = content.index(line) + 1
#                 if next_line_index < len(content) and content[next_line_index].strip().startswith("{"):
#                     new_content.append(line)
#                     new_content.append("```json\n")
#                     inside_entity_recognition = True
#                 else:
#                     new_content.append(line)
#             elif inside_entity_recognition and line.strip().startswith("}"):
#                 new_content.append(line)
#                 new_content.append("```\n")
#                 inside_entity_recognition = False
#             else:
#                 new_content.append(line)
#
#         # 将修改后的内容写回文件
#         with open(filepath, 'w', encoding='utf-8', errors='ignore') as file:
#             file.writelines(new_content)