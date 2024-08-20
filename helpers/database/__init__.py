import psycopg2 
from Globals import DATABASE_NAME

def get_db_connection():
  conn = None
  try:
    conn = psycopg2.connect(database=DATABASE_NAME, user="api_flask", 
                        password="api1234", host="localhost", port="5432")
  except:
    print("Não foi possível conectar ao BD")

  return conn