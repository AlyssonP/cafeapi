"""
    Código principal da aplicação.
"""
from flask import Flask, request, jsonify, g

from helpers.logging import logger
from helpers.database import get_db_connection

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    """
        Função para finalização da conexão ao banco de dados.
        caso o contexto seja destruído a conexão será encerrada.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """
        Função de consulta útil para casos repetitivos.
    """
    cursor = get_db_connection().cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    if one:
        return rv[0] if rv else None
    return rv

@app.route("/")
def index():
    """
          Função do endpoint raiz da aplicação.
      """
    logger.info("Entrou no index da aplicação.")
    return jsonify({"version": 1.0}, 200)

def get_usuarios():
    """
        Função para o endpoint para listagem de usuários.
    """
    usuarios_list = []
    for row in query_db("SELECT * FROM tb_usuario WHERE deleted_at IS NULL"):
        # Convertendo data de nascimento
        nascimento = row[2]
        if nascimento:
            nascimento_formatado = nascimento.strftime('%d/%m/%Y')
        else:
            nascimento_formatado = None
        usuarios_list.append({
        "id": row[0],
        "nome": row[1],
        "nascimento": nascimento_formatado
        })
    return usuarios_list

def get_usuario_by_id(id_usuario):
    """
        Função para buscar usuário por id.
    """
    usuario_dict = None
    linha = query_db(
        "SELECT * FROM tb_usuario WHERE id = %s and deleted_at IS NULL", 
        [id_usuario,],
        True
    )
    if linha is not None:
        usuario_dict = {
            "id": linha[0],
            "nome": linha[1],
            "nascimento": linha[2].strftime('%d/%m/%Y')
        }
    return usuario_dict

def set_usuario(data):
    """
        Função para o endpoint de criação de usuário no banco de dados.
    """
    # Criação do usuário.
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    # Persistir os dados no banco.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tb_usuario(nome, nascimento)'
        'VALUES (%s, %s)'
        ' RETURNING id;',
        (nome, nascimento)
    )
    data['id'] = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    # Retornar o usuário criado.
    return data

def update_usuario(id_usuario, data):
    """
        Função para atualização de dados de usuário.
    """
    # Criação do usuário.
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    # Persistir os dados no banco.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tb_usuario SET nome = %s, nascimento = %s WHERE id = %s and deleted_at IS NULL',
        (nome, nascimento, id_usuario)
        )
    conn.commit()
    rowupdate = cursor.rowcount
    conn.close()
    # Retornar a quantidade de linhas.
    return rowupdate

def delete_fisico_usuario(id_usuario):
    """
        Função responsável por realizar exclução fisica de um usuário por id.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_usuario WHERE id=%s", (id_usuario,))
    conn.commit()
    rowupdate = cursor.rowcount
    conn.close()
    return rowupdate

def delete_logico_usuario(id_usuario):
    """
        Função responsável por realizar exclução lógica de um usuário por id.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tb_usuario SET deleted_at = CURRENT_TIMESTAMP'
        'WHERE id = %s and deleted_at IS NULL;',
        (id_usuario,)
        )
    conn.commit()
    rowupdate = cursor.rowcount
    conn.close()
    return rowupdate

@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios_metodos():
    """
        Função reponsável para gerenciamento de endpoits com métodos GET E POST de usuarios.
    """
    if request.method == 'GET':
        # Listagem dos usuários
        usuarios = get_usuarios()
        return jsonify(usuarios), 200
    elif request.method == 'POST':
        # Recuperar dados da requisição: json.
        data = request.json
        data = set_usuario(data)
        return jsonify(data), 201
    return None

@app.route("/usuarios/<int:id_usuario>", methods=['GET', 'DELETE', 'PUT'])
def usuario_metodos2(id_usuario):
    """
        Função reponsável para gerenciamento de endpoits com métodos GET, DELETE e PUT de usuarios.
    """
    if request.method == 'GET':
        usuario = get_usuario_by_id(id_usuario)
        if usuario is not None:
            return jsonify(usuario), 200
        return {}, 404
    elif request.method == 'PUT':
        # Recuperar dados da requisição: json.
        data = request.json
        rowupdate = update_usuario(id_usuario, data)
        if rowupdate != 0:
            return (data, 201)
        return (data, 304)
    elif request.method == 'DELETE':
        is_logico = request.args.get('isLogico', default='false').lower()
        if is_logico in ('true', '1', 't', 'yes', 'y'):
            response = delete_logico_usuario(id_usuario)
        else:
            response = delete_fisico_usuario(id_usuario)
        if response != 0:
            return jsonify(), 204
        return jsonify({"msg": "Não foi possivel deletar usuário."}), 404
    return None
