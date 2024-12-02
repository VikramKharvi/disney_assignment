from fastapi import FastAPI, Query
import uvicorn
from modules.ingest_data import run_data_ingession_csv,run_data_ingession_pdf
from modules.clean_data import process_cleaning
from modules.ingest_sql import push_sql
from modules.structured_rag import generate_structured_response
from modules.unstructured_rag import generate_unstructured_response
from modules.embed_data import run_embeddings
from modules.create_llm import mistral_llm,openai_llm
app = FastAPI()
openai_api_key="<open ai key>"
hf_token = "<hf key>" 

@app.get("/")
async def process(path,question,type,llm_type):
    if type=='structured':
        df = run_data_ingession_csv(path)
        df = process_cleaning(df)
        push_sql(df)
        response = generate_structured_response(question,openai_api_key)

    if type=='unstructured':
        extracted_data = run_data_ingession_pdf(path)
        vector_store = run_embeddings(extracted_data)
        if llm_type == 'mistral':
            llm = mistral_llm(hf_token)
        else:
            llm = openai_llm(openai_api_key)
        response = generate_unstructured_response(llm,vector_store,question)
        try:
            response = response.content
        except:
            pass

    return {"message": response}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)