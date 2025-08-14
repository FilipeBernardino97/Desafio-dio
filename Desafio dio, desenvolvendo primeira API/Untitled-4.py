routers/atleta.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from starlette.responses import JSONResponse
from fastapi_pagination import Page, paginate
from typing import Optional, List

from database import get_db
from models import Atleta
from schemas import AtletaCreate, AtletaResponse

router = APIRouter(prefix="/atletas", tags=["Atletas"])

@router.post("/", status_code=201)
async def create_atleta(atleta_data: AtletaCreate, db: Session = Depends(get_db)):
    try:
        new_atleta = Atleta(nome=atleta_data.nome, cpf=atleta_data.cpf)
        db.add(new_atleta)
        db.commit()
        db.refresh(new_atleta)
        return new_atleta
    except IntegrityError:
        # Manipula a exceção quando o CPF já existe
        return JSONResponse(
            status_code=303,
            content={"mensagem": f"Já existe um atleta cadastrado com o cpf: {atleta_data.cpf}"}
        )

@router.get("/", response_model=Page[AtletaResponse])
async def get_all_atletas(
    nome: Optional[str] = Query(None, description="Filtrar por nome do atleta"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF do atleta"),
    db: Session = Depends(get_db)
):
    query = select(Atleta)
    
    # Aplica os filtros se os parâmetros de consulta forem fornecidos
    if nome:
        query = query.where(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.where(Atleta.cpf == cpf)
    
    # Usa a função paginate da biblioteca para lidar com limite e offset
    # A biblioteca vai extrair os parâmetros 'limit' e 'offset' da URL automaticamente
    # e aplicar à consulta.
    return paginate(db.execute(query).scalars().all())