import uuid
from typing import Optional

import bcrypt

from database import SessionLocal
from models.usuario import Usuario

usuario_logado: Optional[dict] = None

def login(email: str, password: str) -> Optional[Usuario]:
    global usuario_logado # Torna a variavel global

    with SessionLocal() as session:
        # Filtra no banco de dados por email
        usuario = session.query(Usuario).filter_by(email=email).first()
        # Faz a verificação se a senha que foi criptografada bate com o DB
        if usuario and bcrypt.checkpw(password.encode("utf-8"),
                                      usuario.senha.encode("utf-8")):
            token = str(uuid.uuid4())
            usuario_logado = {
                "id": usuario.id,
                "nome": usuario.nome,
                "role": usuario.role,
                "token": token
            }
            print(f"""
🔓 Login realizado com sucesso!!
Seja bem vindo {usuario.nome}""")
            return usuario_logado
        else:
            print("❌ Email ou senha incorretos.")
            return False

def logout():
    global usuario_logado
    usuario_logado = None
    print("\n Logout realizado com sucesso.")

def listar_usuarios() -> list:
    with SessionLocal() as session:
        try:
            usuarios = session.query(Usuario).all()

            if not usuarios:
                return []
            
            return usuarios
        
        except Exception as e:
            print(f"Erro ao listar usuarios: {e}")
            return []

def cadastrar_usuario(name: str, email: str, senha: str, role: str) -> bool:
    with SessionLocal() as session:
        try:
            if session.query(Usuario).filter_by(email=email).first():
                print("❌ Já existe usuario com esse email.")
                return False
            
            if role not in ["admin", "usuario"]:
                print("❌ Role inválida. Use 'admin' ou 'usuario'.")
                return False
            
            hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
            novo_usuario = Usuario(
                nome=name,
                email=email,
                senha=hashed.decode("utf-8"),
                role = role
            )
            session.add(novo_usuario)
            session.commit()
            print(f"\n✅ Usuario {name} foi criado com sucesso!!")
            return True
        
        except Exception as e:
            session.rollback()
            print("Erro ao Registrar:", e)
            return False
