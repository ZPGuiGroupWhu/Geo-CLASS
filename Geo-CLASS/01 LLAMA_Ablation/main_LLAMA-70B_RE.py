# Calling Meta-Llama-3-70B using the Qianfan model, ablation experiment: entities and relationships are not processed step by step
import os
import qianfan
import Extractor_Constant_LLAMA_RE
from Script_preprocessing import read_and_clean_file

# Set authentication information
os.environ["QIANFAN_ACCESS_KEY"] = "BAIDU_API_KEY"
os.environ["QIANFAN_SECRET_KEY"] = "BAIDU_SECRET_KEY"

chat_comp = qianfan.ChatCompletion()

input_folder = r".\GEE_Samples"
output_folder = r".\LLM_Extraction_Result\LLAMA70B_RE"

# Check if the output folder exists and create it if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the file names in two folders
sample_files = set(os.listdir(input_folder))
result_files = set(os.listdir(output_folder))

# Find files that only exist in sample_dir
files_to_process = sample_files - result_files
print(len(files_to_process))

# Process these files
for file_name in files_to_process:
    if file_name.endswith('.txt'):
        file_path = os.path.join(input_folder, file_name)
        GEE_script = read_and_clean_file(file_path)

        prompt = f'Your role: {Extractor_Constant_LLAMA_RE.role} \n\n' + \
                        f'Your task: {Extractor_Constant_LLAMA_RE.task} \n {GEE_script} \n\n' + \
                        f'Your reply needs to meet these requirements: \n {Extractor_Constant_LLAMA_RE.Requirement_str} \n\n' + \
                        f'Your reply example: {Extractor_Constant_LLAMA_RE.Reply_example} \n\n'

        if len(prompt) > 20000:
            print(f"Error: Input text exceeds maximum limit of 20000 characters. Skipping file {file_name}")
            continue

        resp = chat_comp.do(model="Meta-Llama-3-70B", messages=[{
            "role": "user",
            "content": prompt
        }], temperature=0.2)
        content = resp["body"]
        result = content['result']
        usage = content['usage']

        print(result)

        total_prompt_tokens = usage['prompt_tokens']
        total_completion_tokens = usage['completion_tokens']
        total_tokens = usage['total_tokens']

        total_usage = {
            'prompt_tokens': total_prompt_tokens,
            'completion_tokens': total_completion_tokens,
            'total_tokens': total_tokens
        }

        output_file_path = os.path.join(output_folder, os.path.basename(file_path))
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Entity Recognition:\n{result}\n\nTotal_Usage:\n{total_usage}")
