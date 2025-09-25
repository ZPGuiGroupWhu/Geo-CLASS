# Process the result file into two parts, namely Entity and Relation

# General result: Two-part '''json'' operation
import os
import re

# Modify the input paths according to the result directories of different LLMs
input_folder = r".\LLM_Extraction_Result\GPT3.5"

# Specify the output folder path
# Modify the output paths according to the result directories of different LLMs
output_folder_entity = r".\LLM_Extraction_Result\GPT3.5\Entity"
output_folder_relation = r".\LLM_Extraction_Result\GPT3.5\Relation"
error_log_path = r".\LLM_Extraction_Result\GPT3.5\err.txt"

# If the output folders do not exist, create them
os.makedirs(output_folder_entity, exist_ok=True)
os.makedirs(output_folder_relation, exist_ok=True)

# # Regular expression pattern to find the start of a JSON block
# json_start_pattern = re.compile(r'({)', re.DOTALL)

# Error count and error message list
error_count = 0
error_messages = []


def find_json_blocks(content):
    """Find all JSON blocks from the content"""
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

# Iterate over each file in the input folder
for filename in os.listdir(input_folder):
    # Generate a complete file path
    filepath = os.path.join(input_folder, filename)

    # Make sure the path points to a file, not a folder
    if os.path.isfile(filepath):
        # Read file contents
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

            # Find all JSON blocks
            json_blocks = find_json_blocks(content)
            entity_found = False
            relation_found = False

            # Process each JSON block
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

    # Write error information to the err.txt file
    with open(error_log_path, 'w', encoding='utf-8') as error_file:
        for message in error_messages:
            error_file.write(message + '\n')

    print(f"Total errors: {error_count}")
    print(f"Error details saved to {error_log_path}")
