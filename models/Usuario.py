import json

class Usuario():
  def __init__(self, nome: str, nascimento) -> None:
    self.id = id
    self.nome = nome
    self.nascimento = nascimento
    
class UsuarioEnconder(json.JSONEncoder):
  def default(self, objUsuario):
    if isinstance(objUsuario, Usuario):
      return {"nome": objUsuario.nome, "nascimento": objUsuario}
    return super().default(objUsuario)