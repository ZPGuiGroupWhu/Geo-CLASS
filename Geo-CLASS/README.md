# Geo-CLASS

Geoprocessing Modeling Knowledge Extraction from Crowdsourced Google Earth Engine Scripts by Collaborating Large and Small Language Models.

## 目录

- [Background](#Background)
- [Project Description](#Project Description)

## Background

Online geoinformation platforms produce numerous scripts for specific geospatial analyses. To overcome challenges with large language models in understanding scripts, we propose Geo-CLASS, a framework that integrates the strengths of both large and small language models for knowledge extraction.

## Project Description
### GEE_Samples
GEE scripts used in the experiment.
### 00 Corpus  
Constructed Knowledge Base, including the dimension in Theme, Function and Data Source.
### 01 LLM_Extraction
1. Based on CoT idea, we build Schema-aware program, namely "Extender_Constant.py"
2. Call different large language models for preliminary knowledge extraction.
   Usage Examples:
   ```bash 
   python main_GPT3.5.py
   python main_GPT4O.py
   python main_LLAMA-70B.py
### 01 LLAMA_Ablation
Ablation experiment for no CoT thinking, no entity constraints, no relation constraints, respectively.
### 01 LLAMA_Comparation
Comparative analysis for directly inputting the ontology concepts in the knowledge base as prompts into different large language models for preliminary knowledge extraction.
### LLM_Extraction_Result
Output file storage of preliminary extraction results of large models.
### 02 Json2csv
Convert the txt file of the large model output result into a csv file for storage.
### 03 SLM_Standerlization
1. embedder_corpus:Vectorize the concept ontology in the knowledge base using a small model.
   Usage Examples:
   ```bash 
   python embedder_corpus.py --model 'sentence-transformers/sentence-t5-large' --input '.\00 Corpus\Function_Dictionary.txt' --output '.\03 SLM_Standerlization\function_sentence-t5-large.pth'
   python embedder_corpus.py --model 'sentence-transformers/sentence-t5-large' --input '.\00 Corpus\GCMD.json' --output '.\03 SLM_Standerlization\theme_sentence-t5-large.pth'
   python embedder_corpus.py --model 'BAAI/bge-m3' --input '.\00 Corpus\Function_Dictionary.txt' --output '.\03 SLM_Standerlization\function_baai.pth'
   python embedder_corpus.py --model 'BAAI/bge-m3' --input '.\00 Corpus\GCMD.json' --output '.\03 SLM_Standerlization\theme_baai.pth'
2. func_them_update:Use the small model to vectorize the entity description extracted from the large model, calculate the similarity with the concept vector library of the corresponding ontology library, and pair the entity description with the highest similarity with the ontology concept.
   Usage Examples:
   ```bash 
   python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input '.\Data\GPT3.5\function_sample.csv' --output '.\Data\GPT3.5\function_sample.csv' --embeddings '.\03 SLM_Standerlization\function_sentence-t5-large.pth'
   python func_theme_update.py --model 'BAAI/bge-m3' --input '.\Data\GPT3.5\function_sample.csv' --output '.\Data\GPT3.5\function_sample.csv' --embeddings '.\03 SLM_Standerlization\function_baai.pth'
   python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input '.\Data\GPT3.5\theme_sample.csv' --output '.\Data\GPT3.5\theme_sample.csv' --embeddings '.\03 SLM_Standerlization\theme_sentence-t5-large.pth'
   python func_theme_update.py --model 'BAAI/bge-m3' --input '.\Data\GPT3.5\theme_sample.csv' --output '.\Data\GPT3.5\theme_sample.csv' --embeddings '.\03 SLM_Standerlization\theme_baai.pth'
3. relation_update:
Match the head entity and tail entity descriptions in the relationship triple with the concepts in the ontology library.
### Data
Entity descriptions extracted by different LLMs and the results after standardization by different SLMs
### 04 Estimation
1. get_concept_information_content and get_similarity: calculate the Lin similarity between the standerlized result and the true value
   Usage Examples:
   ```bash 
   scripts_similarity.bat
2. metrics: evaluate the results of collaborative knowledge extraction between large and small models with precision, recall, and F1-score
   Usage Examples:
   ```bash 
   scripts_metrics.bat
   scripts_metrics_relation.bat
### Output
Evaluation results
### figures.ipynb
Integrate and draw the Output
