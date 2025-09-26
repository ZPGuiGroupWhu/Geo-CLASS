@echo off


@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B\function_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B\output_path_function_sentence-t5-large.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B\theme_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B\output_path_theme_sentence-t5-large.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B\function_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B\output_path_function_baai.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B\theme_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B\output_path_theme_baai.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B\function_sample.csv" --value_column "Value_LLAMA70B" --output ".\Output\output_LLAMA70B\output_path_function_llama70b.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B\theme_sample.csv" --value_column "Value_LLAMA70B" --output ".\Output\output_LLAMA70B\output_path_theme_llama70b.csv"

@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\GPT3.5\function_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_GPT3.5\output_path_function_sentence-t5-large.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\GPT3.5\theme_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_GPT3.5\output_path_theme_sentence-t5-large.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\GPT3.5\function_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_GPT3.5\output_path_function_baai.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\GPT3.5\theme_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_GPT3.5\output_path_theme_baai.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\GPT3.5\function_sample.csv" --value_column "Value_GPT3.5" --output ".\Output\output_GPT3.5\output_path_function_gpt3.5.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\GPT3.5\theme_sample.csv" --value_column "Value_GPT3.5" --output ".\Output\output_GPT3.5\output_path_theme_gpt3.5.csv"

@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\GPT4o\function_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_GPT4o\output_path_function_sentence-t5-large.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\GPT4o\theme_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_GPT4o\output_path_theme_sentence-t5-large.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\GPT4o\function_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_GPT4o\output_path_function_baai.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\GPT4o\theme_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_GPT4o\output_path_theme_baai.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\GPT4o\function_sample.csv" --value_column "Value_GPT4o" --output ".\Output\output_GPT4o\output_path_function_gpt4o.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\GPT4o\theme_sample.csv" --value_column "Value_GPT4o" --output ".\Output\output_GPT4o\output_path_theme_gpt4o.csv"
@REM
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B_RE\function_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B_RE\output_path_function_sentence-t5-large.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B_RE\theme_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B_RE\output_path_theme_sentence-t5-large.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B_RE\function_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B_RE\output_path_function_baai.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B_RE\theme_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B_RE\output_path_theme_baai.csv"
@REM
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoE\function_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B_Schema_NoE\output_path_function_sentence-t5-large.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoE\theme_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B_Schema_NoE\output_path_theme_sentence-t5-large.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoE\function_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B_Schema_NoE\output_path_function_baai.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoE\theme_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B_Schema_NoE\output_path_theme_baai.csv"
@REM
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoR\function_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B_Schema_NoR\output_path_function_sentence-t5-large.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoR\theme_sample.csv" --value_column "Value_sentence-t5-large" --output ".\Output\output_LLAMA70B_Schema_NoR\output_path_theme_sentence-t5-large.csv"
@REM python get_similarity3.py --task "function" --file_4 ".\Data\GPT4.0\function_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoR\function_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B_Schema_NoR\output_path_function_baai.csv"
python get_similarity3.py --task "theme" --file_4 ".\Data\GPT4.0\theme_true.csv" --file_35 ".\Data\LLAMA70B_Schema_NoR\theme_sample.csv" --value_column "Value_BAAI" --output ".\Output\output_LLAMA70B_Schema_NoR\output_path_theme_baai.csv"
