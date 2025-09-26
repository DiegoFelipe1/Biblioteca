from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
DB = "sqlite:///./test.db"

engine = create_engine(DB)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "Usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    role = Column(String, default="user")

    #Relação de Usuario com emprestimo
    emprestimos = relationship("Emprestimo", back_populates="usuario")

class Livro(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    autor = Column(String, nullable=False)
    disponivel = Column(Boolean, default=True)

    #Relação de Livros com emprestimo
    emprestimos = relationship("Emprestimo", back_populates="livro")

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

Base.metadata.create_all(bind=engine)

