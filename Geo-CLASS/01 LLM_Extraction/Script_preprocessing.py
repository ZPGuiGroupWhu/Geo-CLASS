# 脚本预处理：删除脚本中的注释代码，保留注释文本，减少token浪费，同时减少大模型的误解，提高大模型的准确性

import os
import re
import time


# 记录开始时间
start_time = time.time()


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            read_and_clean_file(file_path)


def read_and_clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    in_comment_block = False
    comment_block = []

    for line in lines:
        # 检查是否是特殊的单行注释
        if line.strip().startswith('/****') and line.strip().endswith('****/'):
            new_lines.append(line)
            continue
        if line.strip().startswith('/*'):
            in_comment_block = True
            comment_block = [line]
            if line.strip().endswith('*/'):
                in_comment_block = False
                # 检查注释代码块是否包含'https://'或'https://'，或是否符合is_code_block的条件
                if any("https://" in l or "http://" in l for l in comment_block) or not any(
                        is_code_block(l) for l in comment_block):
                    new_lines.extend(comment_block)
                comment_block = []
            continue

        if in_comment_block:
            comment_block.append(line)
            if line.strip().endswith('*/'):
                in_comment_block = False
                # 检查注释代码块是否包含'https://'或'https://'，或是否符合is_code_block的条件
                if any("https://" in l or "http://" in l for l in comment_block) or not any(
                        is_code_block(l) for l in comment_block):
                    new_lines.extend(comment_block)
                comment_block = []
            continue

        if not in_comment_block:
            if "https://" in line or "http://" in line:
                new_lines.append(line)
            else:
                new_lines.append(process_line(line))
        # 您的生成路径
    result = '\n'.join(new_lines)
    return result


def process_line(line):
    match = re.match(r'^(.*?)//(.*)$', line)
    if match:
        before_double_slash = match.group(1)
        after_double_slash = match.group(2)
        if is_code_statement(after_double_slash):
            return before_double_slash + '\n'
    return line


def is_code_statement(text):
    # 如果以, ; { } [ ] 其中之一结尾，则判定为代码行
    if text.strip().endswith((',', ';', '{', '}', '[', ']')):
        return True

    # 一级编程符号
    code_symbols_1 = ['=', '{', '}', '|', '&', ' //']
    # JavaScript 关键字
    js_keywords = ['var ', 'let', 'return', 'print', 'while', 'ee.', 'Map.', 'Export.']
    # 检查符号和关键字
    if any(symbol in text for symbol in code_symbols_1) or any(keyword in text for keyword in js_keywords):
        return True

    # 检查文本是否包含 'ing'
    if 'ing ' in text and '//' not in text:
        return False

    # 检查文本是否以空格加大写字母开头
    if re.match(r'\s+[A-Z]', text):
        return False

    # .后带单词字符(>=2个)组成的函数名后跟一对括号
    if re.search(r'\.\w{2,}\(', text):
        return True

    # 新规则：如果 : 和 '' 同时出现，判定为代码
    if ':' in text and '\'' in text:
        return True

    # 检查是否是以 // 或 # 或空格 开头且全是 // 或 # 或空格的行
    if re.match(r'^(\/\/|#|\s)*$', text):
        return True

    if re.match(r'^/+\s*$', text):
        return True

    return False


def is_code_block(text):
    # 如果以{ } [ ] 其中之一结尾，则判定为代码行
    if text.strip().endswith(('{', '}', '[', ']')):
        return True

    # 一级编程符号
    code_symbols_1 = ['=', '{', '}', '|', '&', ' //']
    # JavaScript 关键字
    js_keywords = ['var ', 'let', 'return', 'print', 'while', 'ee.', 'Map.', 'Export.']
    # 检查符号和关键字
    if any(symbol in text for symbol in code_symbols_1) or any(keyword in text for keyword in js_keywords):
        return True

    # 检查文本是否包含 'ing'
    if 'ing ' in text and '//' not in text:
        return False

    # .后带单词字符(>=2个)组成的函数名后跟一对括号
    if re.search(r'\.\w{2,}\(', text):
        return True

    return False


# # 替换为您的原文件目录路径
# directory_path = 'F:\GEE\group3'
# process_directory(directory_path)

# # 记录结束时间
# end_time = time.time()

# # 计算代码的运行时间
# execution_time = end_time - start_time

# # 打印运行时间
# print(f"代码执行时间为: {execution_time} 秒")