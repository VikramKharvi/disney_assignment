# RAG System Documentation

## Introduction

In this assignment, we will work with two types of datasets:

- **Structured data**: Football dataset from Kaggle.
- **Unstructured data**: Short story from a textbook.

The assignment consists of a FastAPI interface that ingests PDF (unstructured data) or CSV (structured data) files and provides relevant responses from a Retrieval-Augmented Generation (RAG) system. Both open-source and closed-source models are utilized to infer outputs.

---

## Code Structure

```
disney/
├── main.py                # FastAPI server to start the application
├── requirements.txt       # List of required libraries
├── dataset/               # Folder where all datasets will be stored
├── create_dataset.py      # Script to create datasets and store them in the 'dataset' folder
├── modules/
│   ├── clean_data.py      # Cleans data by checking for null values, fixing datatypes, removing duplicates, and unwanted characters
│   ├── create_llm.py      # Creates a local Mistral LLM or uses the ChatGPT API
│   ├── embed_data.py      # Embeds data and returns a vectorstore
│   ├── ingest_data.py     # Reads data from CSV and PDF and returns a dataframe and extracted data respectively
│   ├── ingest_sql.py      # Dumps data from the dataframe into SQLite
│   ├── structured_rag.py  # Generates SQL commands to retrieve data for RAG and provides answers
│   └── unstructured_rag.py# Uses the nearest match in vectorstore to generate answers
```

---

## Design Choices

### Framework
- **FastAPI**: A robust, lightweight, and easy-to-deploy Python framework.

### Programming Language
- **Python**: Chosen for its simplicity, readability, and extensive library ecosystem, enabling quick prototyping and complex algorithm implementations.

### Datasets
- The football dataset (CSV) and PDF dataset are representative of common use cases for RAG in LLMs.

### Language Model (LLM)
- **Mistral 7B Instruct Model**: Chosen for its ease of hosting and high-quality output. Requires a GPU.
- Alternatively, the OpenAI ChatGPT API can be used.

### Embedding Model
- **BGE Small Embedding Model**: Chosen for its high benchmark performance on Hugging Face.

### Database
- **SQLite**: A simple, easy-to-use, and robust database solution.

### Text Splitters
- **Recursive Character Splitter**: Used due to the simple nature of the PDF data.

---

## How to Use

### Prerequisites

- Python version 3.11.4 (or a compatible version).

### Setup

1. **Create a virtual environment**:
   ```bash
   cd disney
   python -m venv venv
   ```
   - For Windows:
     ```bash
     venv\Scripts\activate
     ```
     (If you encounter errors, check the `Set-ExecutionPolicy` or run as Administrator.)
   - For Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

2. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```
   (If you encounter errors, check the Python or pip version, or install libraries directly from the source.)

3. **Create datasets**:
   ```bash
   python create_dataset.py
   ```
   - This will create a `dataset` folder and populate it with CSV and PDF files.

4. **Set up API keys**:
   - For Hugging Face:
     - Generate a token by logging into Hugging Face and navigating to `Settings`.
   - For OpenAI:
     - Add your OpenAI API key if using the ChatGPT API.

5. **Run the server**:
   ```bash
   python main.py
   ```
   - If successful, the server will start.

6. **Send a request**:
   - Open another terminal and use `curl` to test:

#### Structured Data Example:
```bash
curl -G "http://localhost:8000/" \
     --data-urlencode "path=dataset" \
     --data-urlencode "question=who was paid 260000usd?" \
     --data-urlencode "type=structured" \
     --data-urlencode "llm_type=openai"
```
**Sample Result**:
```
The individuals who were paid 260,000 USD are De Gea and I Rakiti.
```

#### Unstructured Data Example:
```bash
curl -G "http://localhost:8000/" \
     --data-urlencode "path=dataset" \
     --data-urlencode "question=What happened on the day of Pablo Neruda?" \
     --data-urlencode "type=unstructured" \
     --data-urlencode "llm_type=openai"
```
**Sample Result**:
```json
{
  "message": "On the day of Pablo Neruda's visit, he spent the morning hunting for big game at second-hand bookstores and purchased an old, dried-out volume at Porter for a high price."
}
```

---

