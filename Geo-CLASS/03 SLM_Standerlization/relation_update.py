"""
利用标准化后的实体对关系进行标准化
"""
import pandas as pd

# 读取 CSV 文件
relation_with_function_path = r'F:\Knowledge Extraction_v2\Data\LLAMA70B\relation_with_function.csv'
# relation_with_time_path = 'F:/GEE/18w抽取结果/result_subset2/result_subset2/Relation/Relation2CSV/relation_with_time.csv'

datasource_sample_path = r'F:\Knowledge Extraction_v2\Data\LLAMA70B\datasource_sample.csv'
function_sample_path = r'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv'
# timescope_sample_path = 'F:/GEE/18w抽取结果/result_subset2/result_subset2/Entity/Entity2CSV/timescope_sample.csv'

relation_df = pd.read_csv(relation_with_function_path)
# relation_df = pd.read_csv(relation_with_time_path)
datasource_df = pd.read_csv(datasource_sample_path)
function_df = pd.read_csv(function_sample_path)
# timescope_df = pd.read_csv(timescope_sample_path)

# 创建映射关系
datasource_map = dict(zip(datasource_df['Value'], datasource_df['Best_Name']))
function_map = dict(zip(function_df['Value'], function_df['Value_LLAMA70B']))
# function_map = dict(zip(function_df['Value'], function_df['Value_BERT0']))

# timescope_map = dict(zip(timescope_df['Value'], timescope_df['Value_update']))

# 添加新列并更新值
relation_df['Head_Entity_update'] = relation_df['Head_Entity'].map(datasource_map)
relation_df['Tail_Entity_update'] = relation_df['Tail_Entity'].map(function_map)
# relation_df['Tail_Entity_update'] = relation_df['Tail_Entity'].map(timescope_map)

# 保存更新后的 DataFrame 到新的 CSV 文件
# output_path = 'F:/GEE/18w抽取结果/result_subset3/result_subset3/Relation/Relation2CSV/relation_with_function_update.csv'
# output_path = 'F:/GEE/18w抽取结果/result_subset2/result_subset2/Relation/Relation2CSV/relation_with_time_update.csv'
output_path = r'F:\Knowledge Extraction_v2\Data\LLAMA70B\relation_with_function_LLAMA70B.csv'
relation_df.to_csv(output_path, index=False)

print(f"Updated relation_with_function saved to {output_path}")
