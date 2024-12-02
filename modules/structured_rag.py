from openai import OpenAI
from langchain_core.prompts import PromptTemplate
import pandas as pd
from sqlalchemy import create_engine

# Create a database connection (replace with your database URL)
engine = create_engine('sqlite:///database/football.db')

def make_sql_prompt(query_str,client):
  make_sql_prompt_tmpl_text = """
  Generate a SQL query to answer the following question from the user:
  \"{query_str}\"

  The SQL query should use only tables with the following SQL definitions:

  Table name: football
  Columns: 'Name', 'Age', 'Nationality', 'Club', 'Value', 'Wage', 'Position', 'Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys'

  Make sure you ONLY output an SQL query and no explanation.
  """
  make_sql_prompt_tmpl = PromptTemplate.from_template(make_sql_prompt_tmpl_text)
  make_sql_prompt = make_sql_prompt_tmpl.format(
      query_str=query_str
  )

  MODEL = "gpt-4o"
  completion = client.chat.completions.create(
      model=MODEL,
      temperature=0.1,
      messages=[
              {
                  "role": "system",
                  "content": "You are expert in creating sql commands from user's questions"
              },
              {
                  "role": "user",
                  "content": make_sql_prompt
              }
          ],
  )
  res = completion.choices[0].message.content.strip().split('```sql')[1].split('```')[0].replace('\n',' ')
  return res

def generate_answers(query_str,resulted_data,client):
  answer_prompt_text = """
Answer the following question based on the answer from sql query:

**question**: "{question}"
**answer from sql query for the question**: "{answer}"
  """
  answer_prompt_text = PromptTemplate.from_template(answer_prompt_text)
  answer_prompt_text = answer_prompt_text.format(
      question=query_str,answer=resulted_data
  )

  MODEL = "gpt-4o"
  completion = client.chat.completions.create(
      model=MODEL,
      temperature=0.1,
      messages=[
              {
                  "role": "system",
                  "content": "You are expert in answering users questions"
              },
              {
                  "role": "user",
                  "content": answer_prompt_text
              }
          ],
  )
  res = completion.choices[0].message.content.strip()
  return res

def generate_structured_response(query_str,openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    sql_statement = make_sql_prompt(query_str,client)
    print('SQL prompt:',sql_statement)
    resulted_data = pd.read_sql(sql_statement, con=engine)
    resulted_data = resulted_data.to_string(index=False)
    answer = generate_answers(query_str,resulted_data,client)
    print('Generated answers: ',answer)
    return answer