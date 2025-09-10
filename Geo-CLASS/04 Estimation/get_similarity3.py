# 计算转换后的抽取结果（标准化后的抽取结果）与真值之间的相似度
# 如果是THEME还是FUNCTION，都用Lin相似度进行计算
import pandas as pd
import json
import argparse
from typing import Dict, List, Tuple
import os

from get_concept_information_content import get_paths_to_root

def load_json_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def getLCA(c1, c2, direct_ancestor, ontology_root_concept):
    if c1 == ontology_root_concept or c2 == ontology_root_concept:
        return ontology_root_concept
    concept1_paths = get_paths_to_root(c1, direct_ancestor, ontology_root_concept)
    concept2_paths = get_paths_to_root(c2, direct_ancestor, ontology_root_concept)
    LCAs = []
    for tmp_c1_path in concept1_paths:
        for tmp_c2_path in concept2_paths:
            i = -1
            while tmp_c1_path[i] == tmp_c2_path[i]:
                i -= 1
                if abs(i) > min(len(tmp_c1_path), len(tmp_c2_path)):
                    break
            i += 1
            LCAs.append(tmp_c1_path[i])
    LCAs_depth = []
    for tmp_LCA in LCAs:
        max_depth = 0
        for tmp_c1_path in concept1_paths:
            if tmp_LCA not in tmp_c1_path:
                continue
            try:
                tmp_depth = len(tmp_c1_path) - tmp_c1_path.index(tmp_LCA)
            except ValueError:
                print(c1, c2, concept1_paths, concept2_paths)
                raise ValueError
            if tmp_depth > max_depth:
                max_depth = tmp_depth
        LCAs_depth.append([tmp_LCA, max_depth])
    LCAs_depth.sort(key=lambda x: x[1], reverse=True)
    return LCAs_depth[0][0]


def get_similarity_Lin(c1, c2, direct_ancestor, ontology_root_concept, concept_information_content):
    if c1 not in concept_information_content:
        c1 = ontology_root_concept
    if c2 not in concept_information_content:
        c2 = ontology_root_concept
    if c1 == c2:
        return c1, 1
    if c1 == ontology_root_concept or c2 == ontology_root_concept:
        return ontology_root_concept, 0
    concept1_ic = concept_information_content[c1]
    concept2_ic = concept_information_content[c2]
    max_depth_LCA = getLCA(c1, c2, direct_ancestor, ontology_root_concept)
    max_depth_LCA_ic = concept_information_content[max_depth_LCA]
    if max_depth_LCA_ic == 0:
        return max_depth_LCA, 0
    if concept1_ic + concept2_ic == 0:
        print(c1, c2)
        raise
    similarity_Lin = 2 * max_depth_LCA_ic / (concept1_ic + concept2_ic)
    # Debugging information
    if similarity_Lin > 1:
        print(f"Warning: Similarity > 1 detected. c1: {c1}, c2: {c2}, max_depth_LCA: {max_depth_LCA}, "
              f"concept1_ic: {concept1_ic}, concept2_ic: {concept2_ic}, max_depth_LCA_ic: {max_depth_LCA_ic}, similarity: {similarity_Lin}")

    return max_depth_LCA, similarity_Lin


def load_extracted_concepts(file_path: str, value_column: str) -> Dict[str, List[str]]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    df = pd.read_csv(file_path)
    df.drop_duplicates(subset=['Script_ID', value_column], inplace=True)
    script_concepts = {}
    for _, row in df.iterrows():
        script_id = row['Script_ID']
        concept = row[value_column]
        if script_id not in script_concepts:
            script_concepts[script_id] = []
        script_concepts[script_id].append(concept)
    return script_concepts

def calculate_best_similarity_pairs(functions_4: List[str], functions_35: List[str], direct_ancestor: dict, ontology_root_concept: str, concept_information_content: dict) -> List[Tuple[str, str, float]]:
    best_pairs = []
    used_concepts_4 = set()
    used_concepts_35 = set()
    pairs = []

    for concept_4 in functions_4:
        for concept_35 in functions_35:
            if concept_4 not in used_concepts_4 and concept_35 not in used_concepts_35:
                _, similarity = get_similarity_Lin(concept_4, concept_35, direct_ancestor, ontology_root_concept, concept_information_content)
                pairs.append((concept_4, concept_35, similarity))

    pairs.sort(key=lambda x: x[2], reverse=True)

    for concept_4, concept_35, similarity in pairs:
        if concept_4 not in used_concepts_4 and concept_35 not in used_concepts_35:
            best_pairs.append((concept_4, concept_35, similarity))
            used_concepts_4.add(concept_4)
            used_concepts_35.add(concept_35)

    for concept_4 in functions_4:
        if concept_4 not in used_concepts_4:
            _, similarity_with_root = get_similarity_Lin(concept_4, ontology_root_concept, direct_ancestor, ontology_root_concept, concept_information_content)
            best_pairs.append((concept_4, ontology_root_concept, similarity_with_root))

    return best_pairs

def main(args):
    task_type = args.task
    file_4_path = args.file_4
    file_35_path = args.file_35
    value_column = args.value_column
    output_path = args.output

    if task_type == 'function':
        direct_ancestors = load_json_data('direct_ancestors_function.json')
        root_concept_file = load_json_data('root_concept_function.json')
        ontology_root_concept = root_concept_file["Root Concept"]
        concept_information_content = load_json_data('concept_information_content_function.json')
    else:  # Assume 'theme'
        direct_ancestors = load_json_data('direct_ancestors_theme.json')
        root_concept_file = load_json_data('root_concept_theme.json')
        ontology_root_concept = root_concept_file["Root Concept"]
        concept_information_content = load_json_data('concept_information_content_theme.json')

    functions_4 = load_extracted_concepts(file_4_path, 'Value')
    # functions_4 = load_extracted_concepts(file_4_path, value_column)
    functions_35 = load_extracted_concepts(file_35_path, value_column)

    results = []
    for script_id in functions_35:
        if script_id in functions_4:
            pairs = calculate_best_similarity_pairs(functions_4[script_id], functions_35[script_id], direct_ancestors, ontology_root_concept, concept_information_content)
            for concept_4, concept_35, similarity in pairs:
                results.append([script_id, concept_4, concept_35, similarity])

    result_df = pd.DataFrame(results, columns=['Script_ID', 'Concept_4', 'Concept_35', 'Similarity'])
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    result_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Semantic Similarity Calculation for Functions or Themes')
    parser.add_argument('--task', type=str, required=True, choices=['function', 'theme'], help='Type of task to perform')
    parser.add_argument('--file_4', type=str, required=True, help='Path to the first input CSV file')
    parser.add_argument('--file_35', type=str, required=True, help='Path to the second input CSV file')
    parser.add_argument('--value_column', type=str, required=True, help='Column name in the second CSV file to use for values')
    parser.add_argument('--output', type=str, required=True, help='Path to the output CSV file')

    args = parser.parse_args()
    main(args)

# Example usage:
# python get_similarity3.py --task function --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\function_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\GPT3.5\function_sample.csv' --value_column 'Value_sentence-t5-large' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_3.5\output_path_function_sentence-t5-large.csv'
# python get_similarity3.py --task theme --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\theme_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\GPT3.5\theme_sample.csv' --value_column 'Value_sentence-t5-large' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_3.5\output_path_theme_sentence-t5-large.csv'
# python get_similarity3.py --task function --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\function_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\GPT3.5\function_sample.csv' --value_column 'Value_BAAI' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_3.5\output_path_function_baai.csv'
# python get_similarity3.py --task theme --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\theme_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\GPT3.5\theme_sample.csv' --value_column 'Value_BAAI' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_3.5\output_path_theme_baai.csv'
# python get_similarity3.py --task function --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\function_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\GPT3.5\function_sample.csv' --value_column 'Value_GPT3.5' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_3.5\output_path_function_gpt3.5.csv'
# python get_similarity3.py --task theme --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\theme_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\GPT3.5\theme_sample.csv' --value_column 'Value_GPT3.5' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_3.5\output_path_theme_gpt3.5.csv'

# python get_similarity3.py --task function --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\function_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv' --value_column 'Value_sentence-t5-large' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_LLAMA70B\output_path_function_sentence-t5-large.csv'
# python get_similarity3.py --task theme --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\theme_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\LLAMA70B\theme_sample.csv' --value_column 'Value_sentence-t5-large' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_LLAMA70B\output_path_theme_sentence-t5-large.csv'
# python get_similarity3.py --task function --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\function_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv' --value_column 'Value_BAAI' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_LLAMA70B\output_path_function_baai.csv'
# python get_similarity3.py --task theme --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\theme_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\LLAMA70B\theme_sample.csv' --value_column 'Value_BAAI' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_LLAMA70B\output_path_theme_baai.csv'
# python get_similarity3.py --task function --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\function_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv' --value_column 'Value_LLAMA70B' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_LLAMA70B\output_path_function_llama70b.csv'
# python get_similarity3.py --task theme --file_4 'F:\Knowledge Extraction_v2\Data\GPT4.0\theme_sample.csv' --file_35 'F:\Knowledge Extraction_v2\Data\LLAMA70B\theme_sample.csv' --value_column 'Value_LLAMA70B' --output 'F:\Knowledge Extraction_v2\Output_sim3\output_LLAMA70B\output_path_theme_llama70b.csv'
