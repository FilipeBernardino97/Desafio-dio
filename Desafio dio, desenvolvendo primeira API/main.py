main.py


from fastapi import FastAPI
from fastapi_pagination import add_pagination

from routers import atleta as atleta_router
from database import Base, engine

# Cria as tabelas do banco de dados (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Adiciona a paginação à aplicação
add_pagination(app)

# Inclui o roteador do atleta na aplicação
app.include_router(atleta_router.router)