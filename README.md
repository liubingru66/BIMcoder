# BIMtoSQL Dataset

## Overview
This repository contains the **BIMtoSQL** dataset, a collection of **1,680 instruction-query language pairs** designed for fine-tuning and evaluating **large language models (LLMs)** in the domain of **Building Information Modeling (BIM) and SQL querying**. The dataset is structured to support both precise and ambiguous user queries, making it suitable for improving **NL2SQL** models for BIM-related tasks.

## Dataset Structure
The dataset is categorized into **three main subsets**, each targeting different query characteristics:

### 1. Training Set (1,200 Entries)
- Contains **12 categories of questions**, with **120 samples per category**.
- Each entry consists of a **natural language instruction** paired with a corresponding **JSON-formatted SQL-like query**.
- Designed to train models to understand BIM-related queries and generate structured responses.

### 2. Precise Question Set (240 Entries)
- Follows the **same format** as the training set.
- Questions have **clear intent**, making them easier for models to interpret and process.
- Useful for evaluating model accuracy in structured BIM queries.

### 3. Ambiguous Question Set (240 Entries)
- Mimics queries from **non-expert users**.
- Questions are **more conversational and less structured**, requiring models to infer missing information.
- Aims to test a model’s ability to handle vague or loosely defined BIM-related queries.

## Fine-Tuning and Experimentation

### 1. Fine-Tuning Process
The fine-tuning experiments were conducted on the **Baidu Qianfan Large Model Platform**. The specific training parameters are detailed in the accompanying research paper. Fine-tuning was performed using **Supervised Fine-Tuning (SFT)** on the training set to adapt the model for BIM-specific SQL query generation.

### 2. Experiment Validation
Model performance was evaluated using two key metrics:
- **Exact Match Accuracy**: Measures the percentage of queries that exactly match the standard query structure.
- **Execution Match Accuracy**: Measures the percentage of queries that can be successfully executed on **BIMserver**, even if they differ from the standard query structure.

Detailed results and analysis can be found in the research paper.

## Usage
The dataset is intended for **fine-tuning and testing large language models** on **BIM-specific NL2SQL tasks**. Users can:

- Train models on the dataset to improve **SQL generation** from natural language.
- Evaluate model performance on both **precise and ambiguous** BIM-related queries.
- Experiment with different prompting strategies and fine-tuning techniques for **domain-specific NLP**.

## Limitations
Due to the **large size of fine-tuned models**, they **cannot be uploaded** to GitHub. However, users can **reproduce the fine-tuning process** using the provided dataset and methodologies described in this repository.

## How to Get Started
1. **Download** the dataset from this repository.
2. **Use the training set** to fine-tune an LLM for BIM-related SQL queries.
3. **Evaluate** the model using the precise and ambiguous question sets.
4. **Experiment** with different pre-trained models and training techniques.


## Contact
For questions, contributions, or collaboration inquiries, please reach out via GitHub Issues.



