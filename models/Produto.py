import json

class Produto():
  def __init__(self, id: int, nome: str, categoria: int, setor: int) -> None:
    self.id = id
    self.nome = nome
    self.categoria = categoria
    self.setor = setor
    
class ProdutoEnconder(json.JSONEncoder):
  def default(self, objPrduto):
    if isinstance(objPrduto, Produto):
      return {"nome": objPrduto.nome, "setor": objPrduto.setor, "categoria": objPrduto.categoria}
    return super().default(objPrduto)