import sqlite3
from Globals import DATABASE_NAME

connection = sqlite3.connect(DATABASE_NAME)

with open('schema.sql') as f:
  connection.executescript(f.read())
  
#ursor = connection.cursor()

#cursor.execute("INSERT INTO tb_usuario(nome, nascimento) VALUES ('Administrador', '2024-07-23')")


connection.close()
