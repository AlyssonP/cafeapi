"""
  Inicia a conexão ao banco de dados.
"""
import psycopg2
from flask import g
from Globals import DATABASE_NAME

def get_db_connection():
    """
        Função que estabelece conexão ao banco de dados utilizando o contexto da aplicação.
        
        Inicialmente tenta obter a conexão de banco de dados armazenada no contexto global g.
        Se a conexão não existir, ela é criada e armazenada na variável g._database.
    """
    from app import app  # Importando dentro da função para evitar a importação circular
    with app.app_context():
        conn = getattr(g, "_database", None)
        if conn is None or conn.closed:
            conn = psycopg2.connect(
                host="127.0.0.1",
                port="5433",
                database=DATABASE_NAME,
                user="postgres",
                password="1234")
        return conn
  