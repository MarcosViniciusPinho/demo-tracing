from sqlalchemy import Column, Integer, String
from .database import Base

class Pessoa(Base):
    __tablename__ = "pessoa"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
