from flask import Flask, request, jsonify

from helpers.logging import logger
from helpers.database import get_db_connection
from models.Usuario import Usuario
from models.Produto import Produto

app = Flask(__name__)

@app.route("/")
def index():
  logger.info("Entrou no index da aplicação.")
  return (jsonify({"version": 1.0}, 200))

def getUsuarios():
  conn = get_db_connection()
  cursor = conn.cursor()
  usuarios = cursor.execute('SELECT * FROM tb_usuario').fetchall()
  res = [{"id": id, "nome": nome, "nascimento": nascimento} for id, nome, nascimento in usuarios]
  #res = [Produto(nome, nascimento) for id, nome, nascimento in usuarios]
  conn.close()
  return res

def getUsuarioById(id):
  usuarioDict = None
  conn = get_db_connection()
  cursor = conn.cursor()
  linha = cursor.execute(f'SELECT * FROM tb_usuario WHERE id = {id}').fetchone()
  
  if (linha is not None):
    usuarioDict = {"id": linha[0], "nome": linha[1], "nascimento": linha[2]}
  conn.close()
  return usuarioDict

def createUsuarios(dataJson):
  nome = dataJson.get("nome")
  nascimento = dataJson.get("nascimento")
  usuario = Usuario(nome, nascimento)
  
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(f'INSERT INTO tb_usuario(nome, nascimento) VALUES ("{usuario.nome}", "{usuario.nascimento}")')
  
  conn.commit()
  
  id = cursor.lastrowid
  data = {"id": id, "nome": usuario.nome, "nascimento": usuario.nascimento}
  
  conn.close()
  return data

def putUsuario(id, dataJson):
  nome = dataJson.get("nome")
  nascimento = dataJson.get("nascimento")
  usuario = Usuario(nome, nascimento)
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute('UPDATE tb_usuario SET nome=?, nascimento=? WHERE id = ?',(usuario.nome, usuario.nascimento, id))
  conn.commit()
  
  rowupdate = cursor.rowcount
  
  conn.close()
  return rowupdate
  
def deleteUsuario(id):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(f"DELETE FROM tb_usuario WHERE id={id}")
  conn.commit()
  
  rowupdate = cursor.rowcount
  
  conn.close()
  return rowupdate

@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
  if request.method == "GET":
    return (jsonify(getUsuarios(), 200))
  elif request.method == "POST":
    data = request.json
    return createUsuarios(data), 200
  
@app.route("/usuarios/<int:id>", methods=["GET", "PUT", "DELETE"])
def usuario(id):
  if request.method == "GET":
    usuarioDict = getUsuarioById(id)
    if(usuarioDict is not None):
      return usuarioDict, 200
    else:
      return jsonify({"msg": "Not Found user"}), 404
  
  elif(request.method == "PUT"):
    data = request.json
    response = putUsuario(id, data)
    if(response >= 1):
      return jsonify({"msg": "Usuário atualizado."}), 201
    else:
      return jsonify({"msg": "Não foi possivel atualizar o usuário."}), 304
  
  elif(request.method == "DELETE"):
    response = deleteUsuario(id)
    if(response >= 1):
      return jsonify(), 204
    else:
      return jsonify({"msg": "Não foi possivel deletar usuário."}), 400

