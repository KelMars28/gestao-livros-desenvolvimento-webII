from sqlalchemy import Column, Integer, String
from models.Geral import Base

class Livro(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)