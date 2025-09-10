"""
将抽取出的维度描述（功能描述、主题描述）通过小模型转换成嵌入向量，与语料库嵌入进行相似度匹配然后映射，实现将抽取的维度描述替换成语料库概念存储在csv中
"""
import torch
import argparse
import pandas as pd
import pickle
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time

# 检查是否有可用的 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

def load_model_and_tokenizer(model_name):
    if model_name.startswith('sentence-transformers'):
        model = SentenceTransformer(model_name)
        tokenizer = None  # SentenceTransformer不需要显式的tokenizer
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name).to(device)
    return model, tokenizer

def embed_entity(entity_text, model, tokenizer, model_name):
    if model_name.startswith('sentence-transformers'):
        embedding = model.encode(entity_text, show_progress_bar=False)
    else:
        entity_text = str(entity_text)
        tokens_input = tokenizer(entity_text, padding=True, return_tensors='pt', truncation=True, max_length=512).to(device)
        with torch.no_grad():
            outputs = model(**tokens_input)
            embeddings = outputs.last_hidden_state[:, 0, :]
            embedding = torch.mean(torch.nn.functional.normalize(embeddings, p=2, dim=1), dim=0).cpu().numpy()
    return embedding

def main(args):
    model_name = args.model
    input_path = args.input
    output_path = args.output
    embeddings_file_path = args.embeddings

    # 读取 embeddings 文件
    with open(embeddings_file_path, 'rb') as f:
        corpus_embeddings = pickle.load(f)

    # 将字典转换为嵌入矩阵和对应的关键词列表
    corpus_keywords = list(corpus_embeddings.keys())
    corpus_matrix = np.array([corpus_embeddings[key] for key in corpus_keywords])
    corpus_tensor = torch.tensor(corpus_matrix).to(device)

    # 加载 transformer 模型和 tokenizer
    model, tokenizer = load_model_and_tokenizer(model_name)

    # 读取 entity_function.csv 或者 entity_theme.csv 文件
    entity_df = pd.read_csv(input_path)

    # 根据模型名称添加新列以存储结果
    if model_name.startswith('sentence-transformers'):
        value_col = f'Value_{model_name.split("/")[-1]}'
        similarity_col = f'Top1_Similarity_{model_name.split("/")[-1]}'
    else:
        value_col = 'Value_BAAI'
        similarity_col = 'Top1_Similarity_BAAI'

    entity_df[value_col] = ""
    entity_df[similarity_col] = 0.0

    # 分批计算相似度
    batch_size = 500
    start_total_time = time.time()
    for index, row in entity_df.iterrows():
        start_time = time.time()
        entity_text = row['Value']

        if entity_text == "None":
            top1_keyword = "None"
            top1_similarity = 1.0
        else:
            entity_embedding = embed_entity(entity_text, model, tokenizer, model_name).reshape(1, -1)  # 转移到 CPU 上进行相似度计算
            max_similarity = -1
            top_keyword = None
            # 分批计算相似度
            for i in range(0, corpus_matrix.shape[0], batch_size):
                batch_matrix = corpus_matrix[i:i + batch_size]
                similarities = cosine_similarity(entity_embedding, batch_matrix).flatten()
                max_batch_index = similarities.argmax()
                if similarities[max_batch_index] > max_similarity:
                    max_similarity = similarities[max_batch_index]
                    top_keyword = corpus_keywords[i + max_batch_index]
            top1_similarity = max_similarity
            top1_keyword = top_keyword

        # 将结果存储在数据框的相应列中
        entity_df.at[index, value_col] = top1_keyword
        entity_df.at[index, similarity_col] = top1_similarity

        end_time = time.time()
        print(f"Processed row {index + 1}/{len(entity_df)}: ID {row['ID']}, Time taken: {end_time - start_time:.2f} seconds")
        print(f"Entity: {row['Value']}, Top1_Keyword: {top1_keyword}, Top1_Similarity: {top1_similarity}")

    end_total_time = time.time()
    print(f"Total time taken for all embeddings: {end_total_time - start_total_time:.2f} seconds")

    # 将结果保存回原始数据框并输出
    entity_df.to_csv(output_path, index=False)
    print(entity_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Semantic Similarity Calculation')
    parser.add_argument('--model', type=str, required=True, help='Model name to use for generating embeddings')
    parser.add_argument('--input', type=str, required=True, help='Input file path')
    parser.add_argument('--output', type=str, required=True, help='Output file path')
    parser.add_argument('--embeddings', type=str, required=True, help='Path to the embeddings file')

    args = parser.parse_args()
    main(args)

# bash
# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\GPT3.5\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\GPT3.5\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\GPT3.5\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\GPT3.5\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_baai.pth'
# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\GPT3.5\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\GPT3.5\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\GPT3.5\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\GPT3.5\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_baai.pth'

# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_baai.pth'
# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_baai.pth'

# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_baai.pth'
# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_RE\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_baai.pth'

# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_baai.pth'
# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoE\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_baai.pth'

# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\function_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\function_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_baai.pth'
# python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_sentence-t5-large.pth'
# python func_theme_update.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\theme_sample.csv' --output 'F:\Knowledge Extraction_v2\Data\LLAMA70B_Schema_NoR\theme_sample.csv' --embeddings 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_baai.pth'