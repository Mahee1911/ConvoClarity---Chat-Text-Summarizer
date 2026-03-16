# **ConvoClarity — AI-Powered Chat & Text Summarize**

https://github.com/user-attachments/assets/e2e653a0-c731-429b-8239-0b3e2098f392

ConvoClarity is an end-to-end Natural Language Processing (NLP) application that converts long conversations, transcripts, or textual discussions into concise summaries using a fine-tuned transformer model.

The project demonstrates a production-style machine learning pipeline, integrating model training, evaluation, and deployment through a FastAPI backend with an interactive web interface.

## **Key Features**

• Dialogue and text summarization using Transformer models
• Fine-tuned PEGASUS (google/pegasus-cnn_dailymail)  
• Modular ML pipeline architecture
• FastAPI REST API for inference
• Modern interactive UI with light/dark mode 
• Clean pipeline-based training workflow


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
