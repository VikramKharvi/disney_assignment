import pandas as pd
from sqlalchemy import create_engine

def push_sql(df):
    engine = create_engine('sqlite:///database/football.db')
    df.to_sql('football', con=engine, if_exists='replace', index=False)
    print("DataFrame has been sent to the database and stored.")