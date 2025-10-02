from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Livro(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    autor = Column(String, nullable=False)
    disponivel = Column(Boolean, default=True)

    #Relação de Livros com emprestimo
    emprestimos = relationship("Emprestimo", back_populates="livro")