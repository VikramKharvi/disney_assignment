import pandas as pd
import re
# Function to clean text
def clean_text(text):
    if isinstance(text, str):  # Check if the value is a string
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
        text = text.strip()  # Remove leading and trailing whitespace
    return text

def process_cleaning(df):
    print(df.isna().sum())
    print(df.dtypes) 
    # Apply the clean_text function to all object (string) columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(clean_text)
    football_df = df.drop_duplicates()
    categorical_columns = ['Nationality', 'Club','Position']
    for col in categorical_columns:
        if col in football_df.columns:
            football_df[col] = football_df[col].astype('category')
    return football_df