DROP TABLE IF EXISTS tb_usuario;
DROP TABLE IF EXISTS tb_produto;
DROP TABLE IF EXISTS tb_setor;
DROP TABLE IF EXISTS tb_categoria;

CREATE TABLE tb_usuario (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL,
  nascimento DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE TABLE tb_setor (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL
);

CREATE TABLE tb_categoria (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL
);

CREATE TABLE tb_produto (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL,
  categoria_id INTEGER NOT NULL REFERENCES tb_categoria(id),
  setor_id INTEGER NOT NULL REFERENCES tb_setor(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

INSERT INTO tb_usuario(nome, nascimento) VALUES ('Administrador', '2024-08-19');
