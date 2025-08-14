models.py

from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Atleta(Base):
    __tablename__ = "atletas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Crie as tabelas no banco de dados
from database import engine
Base.metadata.create_all(bind=engine)