# Geo-CLASS

Geoprocessing Modeling Knowledge Extraction from Crowdsourced Google Earth Engine Scripts by Collaborating Large and Small Language Models.

## Catalogue

- [Background](#background)
- [Project Description](#project-description)

## Background

Online geoinformation platforms produce numerous scripts for specific geospatial analyses. To overcome challenges with large language models in understanding scripts, we propose Geo-CLASS, a framework that integrates the strengths of both large and small language models for knowledge extraction.

## Project Description
### GEE_Samples
GEE scripts used in the experiment.
### 00 Corpus  
Constructed Knowledge Base, including the dimension in Theme, Function and Data Source.
### 01 LLM_Extraction
1. Based on CoT idea, we build Schema-aware program, namely `Extractor_Constant.py`
2. Call different large language models for preliminary knowledge extraction.
   Please make sure to replace the API KEY in your `.env` file with your own.
   Since this code calls the LLAMA-70B model via Qianfan, you also need to replace the placeholders with your own `QIANFAN_ACCESS_KEY` and `QIANFAN_SECRET_KEY` before running the related scripts.
   
   Usage Examples (run under the current folder, i.e., `./01 LLM_Extraction`):
   ```bash 
   python main_GPT3.5.py
   python main_GPT4O.py
   python main_LLAMA-70B.py
### 01 LLAMA_Ablation
1. Ablation experiments for disabling CoT reasoning, entity constraints, and relation constraints are implemented in  
`Extractor_Constant_LLAMA_RE.py`, `Extractor_Constant_LLAMA_Schema_NoE.py`, and `Extractor_Constant_LLAMA_Schema_NoR.py`, respectively.
2. `Script_preprocessing`: remove commented-out code while keeping annotation texts, in order to reduce token usage, minimize misinterpretation by large models, and improve accuracy.  
3. For different ablation experiments, please make sure to replace the API KEY in your `.env` file with your own.  
Since this code calls the LLAMA-70B model via Qianfan, you also need to replace the placeholders with your own `QIANFAN_ACCESS_KEY` and `QIANFAN_SECRET_KEY` before running the related scripts.
   Usage Examples (run under the current folder, i.e., `./01_LLAMA_Ablation`):
   ```bash 
   python main_LLAMA-70B_RE.py
   python main_LLAMA-70B_Schema_NoE.py
   python main_LLAMA-70B_Schema_NoR.py

### 01 LLAMA_Extraction_Comparation
1. Comparative analysis for directly inputting the ontology concepts in the knowledge base as prompts into different large language models for preliminary knowledge extraction.
2. Please make sure to replace the API KEY in your `.env` file with your own.
   Since this code calls the LLAMA-70B model via Qianfan, you also need to replace the placeholders with your own `QIANFAN_ACCESS_KEY` and `QIANFAN_SECRET_KEY` before running the related scripts.
   
   Usage Examples (run under the current folder, i.e., `./01 LLM_Extraction_Comparation`):
   ```bash 
   python main_GPT3.5-function.py
   python main_GPT3.5-theme.py

### LLM_Extraction_Result
Output file storage of preliminary extraction results of large models.

### 02 Json2csv
Convert the txt file of the large model output result into a csv file for storage.
When working with results from different experiments or LLMs, remember to update the input and output file paths accordingly.
1. `result_split_entity_relation.py`: Splits the **entity** and **relation** parts from LLM-generated json results in `.txt` files into separate outputs.  
   Usage Examples:
   ```bash
   python result_split_entity_relation.py
2. `entity2csv`: This script converts the extracted **entity** part from JSON format into structured CSV files.
   Usage Examples:
   ```bash
   python entity2csv.py
3. `relation2csv`: This script converts the extracted **relation** part from JSON format into structured CSV files.
   Usage Examples:
   ```bash
   python relation2csv.py

### 03 SLM_Standerlization
1. `embedder_corpus.py`: Vectorize the concept ontology in the knowledge base using a small model.
   Usage Examples:
   ```bash 
   python embedder_corpus.py --model 'sentence-transformers/sentence-t5-large' --input '.\00 Corpus\Function_Dictionary.txt' --output '.\03 SLM_Standerlization\function_sentence-t5-large.pth'
   python embedder_corpus.py --model 'sentence-transformers/sentence-t5-large' --input '.\00 Corpus\GCMD.json' --output '.\03 SLM_Standerlization\theme_sentence-t5-large.pth'
   python embedder_corpus.py --model 'BAAI/bge-m3' --input '.\00 Corpus\Function_Dictionary.txt' --output '.\03 SLM_Standerlization\function_baai.pth'
   python embedder_corpus.py --model 'BAAI/bge-m3' --input '.\00 Corpus\GCMD.json' --output '.\03 SLM_Standerlization\theme_baai.pth'
   
2. `func_them_update.py`: Use the small model to vectorize the entity description extracted from the large model, calculate the similarity with the concept vector library of the corresponding ontology library, and pair the entity description with the highest similarity with the ontology concept.
   Note: For different experiments, you need to update the input and output file paths according to the corresponding LLM results.
   For detailed usage, please refer to `scripts.bat`.
   Usage Examples:
   ```bash 
   python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input '.\Data\GPT3.5\function_sample.csv' --output '.\Data\GPT3.5\function_sample.csv' --embeddings '.\03 SLM_Standerlization\function_sentence-t5-large.pth'
   python func_theme_update.py --model 'BAAI/bge-m3' --input '.\Data\GPT3.5\function_sample.csv' --output '.\Data\GPT3.5\function_sample.csv' --embeddings '.\03 SLM_Standerlization\function_baai.pth'
   python func_theme_update.py --model 'sentence-transformers/sentence-t5-large' --input '.\Data\GPT3.5\theme_sample.csv' --output '.\Data\GPT3.5\theme_sample.csv' --embeddings '.\03 SLM_Standerlization\theme_sentence-t5-large.pth'
   python func_theme_update.py --model 'BAAI/bge-m3' --input '.\Data\GPT3.5\theme_sample.csv' --output '.\Data\GPT3.5\theme_sample.csv' --embeddings '.\03 SLM_Standerlization\theme_baai.pth'
   
4. `relation_update.py`: Match the head entity and tail entity descriptions in the relationship triple with the concepts in the ontology library.
    Note: For different experiments, you need to update the input and output file paths according to the corresponding LLM results.
    Usage Examples:
    ```bash
    python relation_update.py  

### Data
Entity descriptions extracted by different LLMs and the results after standardization by different SLMs

### 04 Estimation
1. `get_concept_information_content.py` and `get_similarity3.py`: calculate the Lin similarity between the standerlized result and the true value.
   Note: The file path sometimes needs to be modified according to your specific task.
   Usage Examples (`BASE_PATH` can be modified according to your specific situation):
   ```bash 
   scripts_similarity.bat
2. `metrics.py`: evaluate the results of collaborative knowledge extraction between LLMs and SLMs with precision, recall, and F1-score.
   Usage Examples (`BASE_PATH` can be modified according to your specific situation):
   ```bash 
   scripts_metrics.bat
   scripts_metrics_relation.bat

### Output
This directory contains the experimental results for different Large Language Models (LLMs) and strategies.  

- Each **subfolder** corresponds to the results of a specific LLM and strategy.  

- Within each subfolder:  
  - **`.csv` files**: Contain the mapping between ground truth and recognition results under different dimensions, along with their Lin similarity values.  
  - **`.txt` files**: Contain evaluation results for different dimensions, including **Average Precision**, **Average Recall**, **Average F1-Score**, and **Average Semantic Similarity**, calculated under varying thresholds for determining “correct recognition”. 

### Figures
This folder contains the raw experimental result data and the corresponding figures used in the paper.  

- **Figure 8**: *Performance comparison of LLM baselines with their combinations of different SLMs*  
  Generated by running the Jupyter notebook `Figures.ipynb`.  

- **Figure 9**: *Ablation experiments of CoT principle and schema-aware strategy on the Geo-CLASS framework*  
  Created manually using Microsoft Excel based on the experimental data.  

- **Figure 10**: *Performance analysis under varying similarity thresholds on precision, recall, and F1-score*  
  Generated by running the Jupyter notebook `Figures.ipynb`.  

  Usage: To reproduce Figures 8 and 10, open and run the notebook:

   ```bash
   jupyter notebook Figures.ipynb
