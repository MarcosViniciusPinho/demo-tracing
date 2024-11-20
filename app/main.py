from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from .models import Pessoa
from .database import Base, engine, get_db
from pydantic import BaseModel
import uuid
from sqlalchemy import event
from . import init_observability, start_span, set_span_attributes, set_span_record_exception

init_observability(
    service_name="demo-tracing",
    host="localhost:4317"
)

import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

Base.metadata.create_all(bind=engine)

class PessoaCreate(BaseModel):
    nome: str
    sobrenome: str
    idade: int
    cpf: str

class PessoaResponse(PessoaCreate):
    id: int

    class Config:
        from_attributes = True

def trace_db_operations(conn, cursor, statement, parameters, context, executemany):
    with start_span("db", "database-operation") as span:
        set_span_attributes(span, {
            "db.statement": statement,
            "db.parameters": str(parameters),
        })

# Registrando o evento que é disparado após a execução de cada query
@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    trace_db_operations(conn, cursor, statement, parameters, context, executemany)

@app.middleware("http")
async def add_custom_span(request: Request, call_next):
    # Captura o corpo da requisição
    body = await request.body()

    # Converte o corpo para string
    body_str = body.decode("utf-8") 

    # Gere um TID único
    tid = str(uuid.uuid4())

    # Armazene o TID no contexto da requisição
    request.state.tid = tid

    with start_span("fastapi", f"{request.method} {str(request.url)}") as span:
        
        set_span_attributes(span, {
            "http.method": request.method,
            "http.url": str(request.url),
            "http.request.body": body_str,
        })

        response = await call_next(request)

        # Captura o body do response se for texto ou JSON
        if "text" in response.headers.get("content-type", "") or "json" in response.headers.get("content-type", ""):
            # Captura o corpo da resposta
            response_body = [section async for section in response.body_iterator]
            response_body_str = b"".join(response_body).decode("utf-8")

            set_span_attributes(span, {
                "http.response.body": response_body_str,
            })

            # Função auxiliar para criar iterador assíncrono
            async def async_body_iterator():
                for part in response_body:
                    yield part

            # Reseta o iterador para o response ser enviado corretamente
            response.body_iterator = async_body_iterator()
        else:
            # Caso a resposta seja binária ou outro tipo de não-texto
            set_span_attributes(span, {
                "http.response.body": "<non-text response>",
            })

        # Adicione o TID à resposta
        response.headers["X-TID"] = tid
        set_span_attributes(span, {
            "TID": tid,
        })

        return response

@app.post("/pessoas", response_model=PessoaResponse)
def criar_pessoa(request: Request, pessoa: PessoaCreate, db: Session = Depends(get_db)):

    try:

        # Acesse o TID do request
        tid = request.state.tid

        db_pessoa = Pessoa(**pessoa.dict())
        
        db.add(db_pessoa)
        db.commit()
        db.refresh(db_pessoa)

    except SQLAlchemyError as e:
        error = str(e)
        print(f"Erro ao executar operação no banco de dados: {error}")
        with start_span("db", "SQLAlchemyError") as span:
            set_span_record_exception(span, {
                "error": error,
                "TID": tid,
                "Cause": "SQLAlchemyError",
            })
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar pessoa")
    
    except Exception as e:
        error = str(e)
        print(f"Erro inesperado: {error}")
        with start_span("db", "Exception") as span:
            set_span_record_exception(span, {
                "error": error,
                "TID": tid,
                "Cause": "Exception",
            })
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro inesperado")

    return db_pessoa

@app.get("/pessoas", response_model=List[PessoaResponse])
def listar_pessoas(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
     # Acesse o TID do request
    tid = request.state.tid

    person = db.query(Pessoa).offset(skip).limit(limit).all()
    return person
