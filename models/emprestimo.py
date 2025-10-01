from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from ..database import Base

class Emprestimo(Base):
    __tablename__ = "Emprestimos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("Usuarios.id"))
    livro_id = Column(Integer, ForeignKey("Livros.id"))
    data_emprestimo = Column(DateTime, default=datetime.now)
    data_devolucao = Column(DateTime, nullable=True)

    #Relação de emprestimos com livros e usuarios
    usuario = relationship("Usuario", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos")