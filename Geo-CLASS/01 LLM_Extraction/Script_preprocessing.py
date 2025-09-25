# Script preprocessing: Delete the comment code in the script, retain the comment text, reduce token waste, reduce misunderstanding of the large model, and improve the accuracy of the large model

import os
import re
import time


# Recording start time
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
        # Checks if it is a special single-line comment
        if line.strip().startswith('/****') and line.strip().endswith('****/'):
            new_lines.append(line)
            continue
        if line.strip().startswith('/*'):
            in_comment_block = True
            comment_block = [line]
            if line.strip().endswith('*/'):
                in_comment_block = False
                # Checks if the commented code block contains 'https://' or 'https://', ​​or meets the is_code_block condition
                if any("https://" in l or "http://" in l for l in comment_block) or not any(
                        is_code_block(l) for l in comment_block):
                    new_lines.extend(comment_block)
                comment_block = []
            continue

        if in_comment_block:
            comment_block.append(line)
            if line.strip().endswith('*/'):
                in_comment_block = False
                # Checks if the commented code block contains 'https://' or 'https://', ​​or meets the is_code_block condition
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
        # Your build path
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
    # If it ends with one of , ; { } [ ], it is considered a code line
    if text.strip().endswith((',', ';', '{', '}', '[', ']')):
        return True

    # Level 1 programming symbols
    code_symbols_1 = ['=', '{', '}', '|', '&', ' //']
    # JavaScript Keywords
    js_keywords = ['var ', 'let', 'return', 'print', 'while', 'ee.', 'Map.', 'Export.']
    # Checking symbols and keywords
    if any(symbol in text for symbol in code_symbols_1) or any(keyword in text for keyword in js_keywords):
        return True

    # Checks if text contains 'ing'
    if 'ing ' in text and '//' not in text:
        return False

    # Checks if text starts with a space and a capital letter
    if re.match(r'\s+[A-Z]', text):
        return False

    # . followed by a function name consisting of a word character (>= 2) followed by a pair of brackets
    if re.search(r'\.\w{2,}\(', text):
        return True

    # New rule: If : and '' appear at the same time, it is considered a code
    if ':' in text and '\'' in text:
        return True

    # Check if the line starts with // or # or space and is entirely // or # or space
    if re.match(r'^(\/\/|#|\s)*$', text):
        return True

    if re.match(r'^/+\s*$', text):
        return True

    return False


def is_code_block(text):
    # If it ends with one of { } [ ], it is considered a code line
    if text.strip().endswith(('{', '}', '[', ']')):
        return True

    # Level 1 programming symbols
    code_symbols_1 = ['=', '{', '}', '|', '&', ' //']
    # JavaScript Keywords
    js_keywords = ['var ', 'let', 'return', 'print', 'while', 'ee.', 'Map.', 'Export.']
    # Checking symbols and keywords
    if any(symbol in text for symbol in code_symbols_1) or any(keyword in text for keyword in js_keywords):
        return True

    # Checks if text contains 'ing'
    if 'ing ' in text and '//' not in text:
        return False

    # . followed by a function name consisting of a word character (>= 2) followed by a pair of brackets
    if re.search(r'\.\w{2,}\(', text):
        return True

    return False


# # Replace with your original file directory path
# directory_path = 'Your_directory_path'
# process_directory(directory_path)

# # Record end time
# end_time = time.time()

# # Calculate the running time of the code
# execution_time = end_time - start_time

# # Print running time
# print(f"The code execution time is: {execution_time} 秒")
