# 对样本集进行二次筛选后的评估
import argparse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_recall_fscore_support


# 评估功能或主题维度抽取的效果
def compute_function_theme_metrics(output_path, txt_file_path):
    # 不过滤输出数据，保留所有条目
    # 读取数据
    output_df = pd.read_csv(output_path)

    # 获取 output_path 中存在的 Script_ID
    valid_script_ids = output_df['Script_ID'].unique()

    # 过滤 output_df 以只包含这些 Script_ID
    filtered_output_df = output_df[output_df['Script_ID'].isin(valid_script_ids)].copy()

    # 确保数据按 Script_ID 排序
    filtered_output_df.sort_values("Script_ID", inplace=True)

    # 将数据转换为字典，键为 Script_ID，值为功能列表
    truth_dict = filtered_output_df.groupby("Script_ID")["Concept_4"].apply(list).to_dict()
    result_dict = filtered_output_df.groupby("Script_ID")["Concept_35"].apply(list).to_dict()

    # 统计 output_new_df 中每个 Script_ID 的 Similarity > 0.8 的数量(为真阳数量)
    true_positive_counts = filtered_output_df[filtered_output_df['Similarity'] > 0.8].groupby('Script_ID').size().to_dict()
    average_similarity = filtered_output_df['Similarity'].mean()


    # 初始化指标
    precision_list, recall_list, f1_scores_list = [], [], []

    # 遍历每个 Script_ID，计算指标
    for script_id in truth_dict.keys():
        truth_set = set(truth_dict[script_id])
        result_set = set(result_dict.get(script_id, []))
        true_positive = true_positive_counts.get(script_id, 0)
        precision = true_positive / len(result_set) if result_set else 0
        recall = true_positive / len(truth_set) if truth_set else 0
        f1_score = 2 * precision * recall / (precision + recall) if precision + recall else 0

        precision_list.append(precision)
        recall_list.append(recall)
        f1_scores_list.append(f1_score)

    # 计算平均指标
    average_precision = sum(precision_list) / len(precision_list) if precision_list else 0
    average_recall = sum(recall_list) / len(recall_list) if recall_list else 0
    average_f1_score = sum(f1_scores_list) / len(f1_scores_list) if f1_scores_list else 0

    print("Average Precision: ", average_precision)
    print("Average Recall: ", average_recall)
    print("Average F1-Score: ", average_f1_score)
    print("Average Semantics Similarity: ", average_similarity)

    # 生成txt文件的路径
    # 打开txt文件并写入内容
    with open(txt_file_path, "w") as file:
        file.write(f"Average Precision: {average_precision}\n")
        file.write(f"Average Recall: {average_recall}\n")
        file.write(f"Average F1-Score: {average_f1_score}\n")
        file.write(f"Average Semantics Similarity: {average_similarity}\n")

    print(f"Results have been saved to {txt_file_path}")


# 评估数据源维度抽取的效果
def compute_datasource_metrics(truth_path, result_path):
    # 读取数据
    truth_df = pd.read_csv(truth_path)
    result_df = pd.read_csv(result_path)

    # 填充 NaN 值为 "None"
    truth_df['Best_Name'] = truth_df['Best_Name'].fillna("None")
    result_df['Best_Name'] = result_df['Best_Name'].fillna("None")

    # 获取所有脚本的 Script_ID
    script_ids = result_df['Script_ID'].unique()

    # 初始化指标
    precision_list, recall_list, f1_scores_list = [], [], []

    # 初始化 TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # 遍历每个 Script_ID，计算指标
    for script_id in script_ids:
        truth_texts = truth_df[truth_df['Script_ID'] == script_id]['Best_Name'].tolist()
        result_texts = result_df[result_df['Script_ID'] == script_id]['Best_Name'].tolist()

        # 计算 tf-idf
        all_texts = truth_texts + result_texts
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        # 分割 tf-idf 矩阵为真值和结果
        truth_tfidf = tfidf_matrix[:len(truth_texts)]
        result_tfidf = tfidf_matrix[len(truth_texts):]

        # 计算 Precision, Recall, F1-Score
        y_true = [1] * len(truth_texts) + [0] * len(result_texts)
        y_pred = [1] * len(result_texts) + [0] * len(truth_texts)
        precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')

        precision_list.append(precision)
        recall_list.append(recall)
        f1_scores_list.append(f1_score)

    # 计算平均指标
    average_precision = sum(precision_list) / len(precision_list)
    average_recall = sum(recall_list) / len(recall_list)
    average_f1_score = sum(f1_scores_list) / len(f1_scores_list)

    print("Average Precision: ", average_precision)
    print("Average Recall: ", average_recall)
    print("Average F1-Score: ", average_f1_score)


# 把得到的output_path_fuction中的function_pair加到抽取的relation文件中，对其进行扩展
def update_tail_entity_pairs(relation_path, concept_path):
    # 读取概念对数据
    concept_df = pd.read_csv(concept_path)
    concept_mapping = concept_df.set_index('Concept_35')['Concept_4'].to_dict()

    # 读取关系数据
    relation_df = pd.read_csv(relation_path)

    # 添加 Tail_Entity_update_pair 列
    relation_df['Tail_Entity_update_pair'] = relation_df['Tail_Entity_update'].map(concept_mapping).fillna(relation_df['Tail_Entity_update'])

    # 保存更新后的关系数据
    relation_df.to_csv(relation_path, index=False)
    return relation_df


# 评估关系识别效果(全匹配)
def compute_relation_metrics(truth_path, result_path, txt_file_path):
    # 读取数据
    truth_df = pd.read_csv(truth_path)
    result_df = pd.read_csv(result_path)

    # 合并两个DataFrame以便比较
    merged_df = pd.merge(truth_df, result_df, left_on=['Script_ID', 'Head_Entity_update', 'Tail_Entity_update'],
                         right_on=['Script_ID', 'Head_Entity_update', 'Tail_Entity_update_pair'], how='inner')

    # 计算指标
    total_truth = len(truth_df)
    total_result = len(result_df)
    true_positive = len(merged_df)

    precision = true_positive / total_result if total_result else 0
    recall = true_positive / total_truth if total_truth else 0
    f1_score = 2 * precision * recall / (precision + recall) if precision + recall else 0

    # 打印结果
    print("Relation Extraction Metrics:")
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1-Score: ", f1_score)

    # 写入结果到txt文件
    with open(txt_file_path, "w") as file:
        file.write(f"Precision: {precision}\n")
        file.write(f"Recall: {recall}\n")
        file.write(f"F1-Score: {f1_score}\n")

    print(f"Results have been saved to {txt_file_path}")



# entity
def main(function_output_path, function_txt_path, theme_output_path, theme_txt_path):
    print("Function Metrics:")
    compute_function_theme_metrics(function_output_path, function_txt_path)
    print("Theme Metrics:")
    compute_function_theme_metrics(theme_output_path, theme_txt_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--function_output_path', type=str, required=True, help='The path to the function output csv file.')
    parser.add_argument('--function_txt_path', type=str, required=True, help='The path to the function output txt file.')
    parser.add_argument('--theme_output_path', type=str, required=True, help='The path to the theme output csv file.')
    parser.add_argument('--theme_txt_path', type=str, required=True, help='The path to the theme output txt file.')
    args = parser.parse_args()
    main(args.function_output_path, args.function_txt_path, args.theme_output_path, args.theme_txt_path)

# python metrics2.py --function_output_path /path/to/function/output.csv --function_txt_path /path/to/function/output.txt --theme_output_path /path/to/theme/output.csv --theme_txt_path /path/to/theme/output.txt


# # relation
# def main(relation_truth_path, relation_result_path, concept_path, relation_txt_path):
#     update_tail_entity_pairs(relation_result_path, concept_path)
#
#     print("Relation Metrics:")
#     compute_relation_metrics(relation_truth_path, relation_result_path, relation_txt_path)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Process some integers.')
#     parser.add_argument('--relation_truth_path', type=str, required=True,
#                         help='The path to the truth relation csv file.')
#     parser.add_argument('--relation_result_path', type=str, required=True,
#                         help='The path to the result relation csv file.')
#     parser.add_argument('--concept_path', type=str, required=True, help='The path to the concept csv file.')
#     parser.add_argument('--relation_txt_path', type=str, required=True, help='The path to the relation output file.')
#     args = parser.parse_args()
#     main(args.relation_truth_path, args.relation_result_path, args.concept_path, args.relation_txt_path)

# python metrics2.py --relation_truth_path "F:/GEE/GEE量化样本01/Experiment/sample_241_4.0/Relation/Relation2CSV/relation_with_function_baai.csv" --relation_result_path "F:\GEE\GEE量化样本01\Experiment\sample_241_LLAMA70B\Relation\Relation2CSV\relation_with_function_baai.csv" --concept_path "F:/Knowledge Extraction/04 Estimation/output_LLAMA70B/output_path_function_baai.csv"
