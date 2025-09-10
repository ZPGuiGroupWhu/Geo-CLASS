"""
把完整语料库Function_Dictionary.txt以及GCMD.json通过小模型BAAI/bge-m3和sentence-transformers/sentence-t5-large进行句子嵌入转换成语义向量，
"""
import os
import json
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import time
import pickle
import argparse

# 递归函数来提取所有的键
def extract_keys(data, keys_list):
    if isinstance(data, dict):
        for key, value in data.items():
            keys_list.append(key)
            extract_keys(value, keys_list)
    elif isinstance(data, list):
        for item in data:
            extract_keys(item, keys_list)

class KeywordEmbedder:
    def __init__(self, model_name='BAAI/bge-m3'):
        self.model_name = model_name
        if model_name.startswith('sentence-transformers'):
            self.model = SentenceTransformer(model_name)
            self.tokenizer = None
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)

    def embed_keywords(self, keywords, output_file_path):
        start_total_time = time.time()

        embeddings_index = {}
        for i, keyword in enumerate(keywords):
            start_time = time.time()

            if self.model_name.startswith('sentence-transformers'):
                # 嵌入整个关键词字符串 (sentence-transformers)
                embedding = self.model.encode(keyword, show_progress_bar=False)
            else:
                # 嵌入整个关键词字符串 (BAAI/bge-m3)
                tokens_input = self.tokenizer(keyword, padding=True, return_tensors='pt', truncation=True, max_length=512)
                with torch.no_grad():
                    outputs = self.model(**tokens_input)
                    embeddings = outputs.last_hidden_state[:, 0, :]
                    embedding = torch.mean(torch.nn.functional.normalize(embeddings, p=2, dim=1), dim=0).cpu().numpy()

            embeddings_index[keyword] = embedding

            end_time = time.time()
            print(f"Time taken for embedding index {i + 1} ({keyword}): {end_time - start_time:.2f} seconds")

        end_total_time = time.time()
        print(f"Total time taken for all embeddings: {end_total_time - start_total_time:.2f} seconds")

        # 保存嵌入字典
        self.save_embeddings(embeddings_index, output_file_path)

        return embeddings_index

    def save_embeddings(self, embeddings, file_name):
        print(f"Saving embeddings to {file_name}...")
        with open(file_name, 'wb') as f:
            pickle.dump(embeddings, f)
        print(f"Embeddings saved successfully to {file_name}.")

# 外部知识库的嵌入处理
def embedding_knowledge_base(input_file_path, output_file_path, model_name):
    # 读取输入文件，并将所有 key 保存到 theme 列表中
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    keys = []
    extract_keys(input_data, keys)
    print(f"Total number of keys: {len(keys)}")

    # 实例化嵌入生成器并生成嵌入
    embedder = KeywordEmbedder(model_name)
    embeddings_index = embedder.embed_keywords(keys, output_file_path)

    # 打印每个嵌入的大小
    for keyword, embedding in embeddings_index.items():
        print(f"Keyword: {keyword}, Embedding size: {embedding.shape}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Keyword Embedding Generator')
    parser.add_argument('--model', type=str, required=True, help='Model name to use for generating embeddings')
    parser.add_argument('--input', type=str, required=True, help='Input file path')
    parser.add_argument('--output', type=str, required=True, help='Output file path')

    args = parser.parse_args()

    # 检查输出路径
    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))
        print(f"Created output directory {os.path.dirname(args.output)}")

    embedding_knowledge_base(args.input, args.output, args.model)

# bash
# python embedder_corpus.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\Function_Dictionary.txt' --output 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_sentence-t5-large.pth'
# python embedder_corpus.py --model 'sentence-transformers/sentence-t5-large' --input 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\GCMD.json' --output 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_sentence-t5-large.pth'
# python embedder_corpus.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\Function_Dictionary.txt' --output 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\function_baai.pth'
# python embedder_corpus.py --model 'BAAI/bge-m3' --input 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\GCMD.json' --output 'F:\Knowledge Extraction_v2\03 SLM_Standerlization\theme_baai.pth'
