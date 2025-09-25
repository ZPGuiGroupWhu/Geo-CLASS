"""
Standardize relations using standardized entities
Note: You need to modify the input and output folder paths according to the extraction results of different LLMs.
"""
import pandas as pd

# Read CSV files
relation_with_function_path = r'.\Data\LLAMA70B\relation_with_function.csv'

datasource_sample_path = r'.\Data\LLAMA70B\datasource_sample.csv'
function_sample_path = r'.\Data\LLAMA70B\function_sample.csv'

relation_df = pd.read_csv(relation_with_function_path)
datasource_df = pd.read_csv(datasource_sample_path)
function_df = pd.read_csv(function_sample_path)

# Create mapping relationships
datasource_map = dict(zip(datasource_df['Value'], datasource_df['Best_Name']))
function_map = dict(zip(function_df['Value'], function_df['Value_LLAMA70B']))

# Add new columns and update values
relation_df['Head_Entity_update'] = relation_df['Head_Entity'].map(datasource_map)
relation_df['Tail_Entity_update'] = relation_df['Tail_Entity'].map(function_map)

# Save the updated DataFrame to a new CSV file
output_path = r'.\Data\LLAMA70B\relation_with_function_LLAMA70B.csv'
relation_df.to_csv(output_path, index=False)

print(f"Updated relation_with_function saved to {output_path}")
