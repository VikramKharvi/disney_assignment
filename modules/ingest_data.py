import pandas as pd
from langchain_community.document_loaders import PyMuPDFLoader

def run_data_ingession_csv(path):
    football_df = pd.read_csv(path+'/football_mini.csv',index_col=False)
    football_df = football_df.drop(football_df.columns[0], axis=1)
    football_df = football_df.iloc[:, : 12]
    return football_df

def run_data_ingession_pdf(path):
    file_name = path+'/story.pdf'
    loader = PyMuPDFLoader(file_name)
    extracted_data = loader.load()
    return extracted_data
