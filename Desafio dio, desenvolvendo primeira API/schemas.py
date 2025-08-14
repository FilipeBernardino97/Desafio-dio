schemas.py


from pydantic import BaseModel
from typing import Optional

class AtletaCreate(BaseModel):
    nome: str
    cpf: str

class AtletaResponse(BaseModel):
    nome: str
    cpf: str
    
    class Config:
        from_attributes = True