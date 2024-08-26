"""
    Codígo reponsável pela construção do banco de dados.
"""
from helpers.database import get_db_connection

with open('schema.sql', encoding="UTF-8") as f:
    shema_sql = f.read()

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(shema_sql)
conn.commit()
cursor.close()
conn.close()
