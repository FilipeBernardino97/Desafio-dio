README.md

# Projeto Workout API

Este projeto é uma API RESTful desenvolvida como parte do bootcamp da Digital Innovation One (DIO). A API gerencia dados de atletas e centros de treinamento, com foco na implementação de boas práticas como organização de código, tratamento de erros e recursos avançados de consulta.

A API foi construída utilizando o framework **FastAPI** e utiliza **SQLAlchemy** para a comunicação com um banco de dados **SQLite**.

## Funcionalidades Implementadas

As seguintes funcionalidades foram desenvolvidas seguindo as instruções do projeto:

-   **API com endpoints para a entidade `Atleta`**.
-   **Validação de Dados**: Uso de modelos Pydantic para validação de entrada e saída.
-   **Tratamento de Erros**:
    -   Captura de `sqlalchemy.exc.IntegrityError` (para CPF duplicado).
    -   Retorno de uma mensagem personalizada e status code `303` para o erro.
-   **Filtragem de Dados**:
    -   Uso de parâmetros de consulta (`query parameters`) para buscar atletas por `nome` e `cpf`.
-   **Paginação**:
    -   Implementação de paginação utilizando a biblioteca `fastapi-pagination`.
    -   Suporte para os parâmetros `limit` e `offset` nos endpoints.

## Tecnologias Utilizadas

-   **FastAPI**: Framework web de alta performance.
-   **Uvicorn**: Servidor ASGI para rodar a aplicação.
-   **SQLAlchemy**: ORM (Mapeador Objeto-Relacional) para interação com o banco de dados.
-   **SQLite**: Banco de dados leve e sem servidor.
-   **fastapi-pagination**: Biblioteca para adicionar paginação aos endpoints.
-   **Pydantic**: Biblioteca para validação de dados.

## Estrutura do Projeto

A estrutura de pastas foi organizada para manter o código limpo e escalável: