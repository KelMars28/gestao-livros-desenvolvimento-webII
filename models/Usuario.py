from sqlalchemy import Column, Integer, String
from models.Geral import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    login = Column(String(20), nullable=False)
    senha = Column(String(20), nullable=False)