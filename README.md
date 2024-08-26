# CafeAPI

**CafeAPI** é uma aplicação desenvolvida como parte de uma atividade avaliativa para a disciplina de Programação Web 2. O projeto visa demonstrar os conhecimentos adquiridos e aplicar os conceitos fundamentais de desenvolvimento de APIs RESTful utilizando o framework Flask em conjunto com PostgreSQL.

## Tecnologias Utilizadas
- **Flask:** Framework web para construção da API.
- **Psycopg2:** Adaptador de banco de dados PostgreSQL para Python.
- **PostgreSQL:** Sistema de gerenciamento de banco de dados relacional.

## Configuração e Execução
1. **Criar Ambiente Virtual (venv)**:
   - Cria um ambiente virtual isolado para instalar as dependências do projeto sem afetar o sistema global.

   Ubuntu
    ```
    virtualenv venv
    ```

2. **Ativar o Ambiente Virtual**:
   - Ativa o ambiente virtual, permitindo que você instale pacotes e execute a aplicação no contexto desse ambiente.

   Ubuntu
    ```
    source venv/bin/activate
    ```

3. **Instalar Dependências**:
   - Instala as bibliotecas e pacotes listados no arquivo `requirements.txt`, que são necessários para a aplicação.
    ```
    pip install -r requirements.txt
    ```
4. **Executar a Aplicação**:
   - Inicia a aplicação Flask.
   ```
   flask run
   ```

## Configuração do Docker (opcional)
Se preferir utilizar o Docker, você pode criar um container com PostgreSQL utilizando o seguinte comando:
```
docker-compose up -d
```