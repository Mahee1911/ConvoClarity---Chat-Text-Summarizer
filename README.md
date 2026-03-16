# **ConvoClarity — AI-Powered Chat & Text Summarize**

https://github.com/user-attachments/assets/e2e653a0-c731-429b-8239-0b3e2098f392

ConvoClarity is an end-to-end Natural Language Processing (NLP) application that converts long conversations, transcripts, or textual discussions into concise summaries using a fine-tuned transformer model.

The project demonstrates a production-style machine learning pipeline, integrating model training, evaluation, and deployment through a FastAPI backend with an interactive web interface.

## **Key Features**

- Dialogue and text summarization using Transformer models
- Fine-tuned PEGASUS (google/pegasus-cnn_dailymail)   M
- Modular ML pipeline architecture
- FastAPI REST API for inference
- Modern interactive UI with light/dark mode
- Clean pipeline-based training workflow


## **Machine Learning Pipeline**

The project follows a structured five-stage ML pipeline architecture, ensuring modularity and reproducibility.

```
Raw Dataset
    │
    ▼
Data Ingestion
    │
    ▼
Data Validation
    │
    ▼
Data Transformation
    │
    ▼
Model Training (Fine-tuning)
    │
    ▼
Model Evaluation
    │
    ▼
Inference API
    │
    ▼
Frontend Application
```
Each stage is implemented as an independent pipeline component, allowing scalable experimentation and maintainability.

## **Pipeline Stages**

### **1. Data Ingestion**
- Downloads and organizes the SAMSum dialogue dataset
- Stores raw data artifacts for further processing

### **2. Data Validation**
- Performs schema checks
- Ensures dataset consistency
- Detects missing or corrupted data

### **3. Data Transformation**
- Tokenizes conversations using HuggingFace AutoTokenizer
- Formats input sequences for model training
- Splits dataset into train, validation, and test sets

### **4. Model Training**
- Fine-tunes PEGASUS (google/pegasus-cnn_dailymail)
- Uses HuggingFace Trainer API
- Saves trained model and tokenizer artifacts

### **5. Model Evaluation**
- Evaluates model performance using ROUGE metrics
- Metrics include ROUGE-1, ROUGE-2, ROUGE-L, and ROUGE-Lsum

### **6. Data Ingestion**
- Downloads and organizes the SAMSum dialogue dataset
- Stores raw data artifacts for further processing

## **Model Architecture**
The system uses the PEGASUS Transformer, designed specifically for abstractive summarization.

Model: `google/pegasus-cnn_dailymail`
Fine-tuned on: `SAMSum Dialogue Dataset`

## **Technologies Used**
### **Machine Learning & NLP**
- Python
- PyTorch
- HuggingFace Transformers
- HuggingFace Datasets
- Evaluate

### **Backend**
- FastAPI
- Uvicorn

### **Machine Learning & NLP**
- HTML
- CSS
- JavaScript

## **Conclusion**

The main objective of this project is to design and understand a **modular machine learning pipeline** for dialogue summarization. The system demonstrates how different stages such as **data ingestion, validation, transformation, model training, and evaluation** can be organized into a structured workflow.

This project focuses on building a **production-style ML pipeline architecture**, making the codebase modular, scalable, and easy to maintain. By exploring the repository, you can see how each pipeline component is implemented and connected to create an end-to-end summarization system.
