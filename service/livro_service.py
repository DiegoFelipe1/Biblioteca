from models.livro import Livro
from models.usuario import Usuario
from models.emprestimo import Emprestimo
from database import SessionLocal

def listar_livros() -> list:
    with SessionLocal() as session:
        livros = session.query(Livro).all()
        
        if not livros:
            return []
            
        return livros
        
def adicionar_livro(titulo: str, autor: str, ano: int) -> bool:
    with SessionLocal() as session:
        try:
            if not titulo:
                print("Por favor digite um titulo")
                return False
            if not autor:
                print("Por favor, digite um autor")
                return False
            if not ano:
                print("Por favor digite um ano.")
                return False
            
            novo_livro = Livro(
                titulo=titulo,
                ano=ano, 
                autor=autor
            )
            session.add(novo_livro)
            session.commit()

            print(f"✅ O livro {titulo} foi adicionado com sucesso")
            return True
        
        except Exception as e:
            session.rollback()
            print("Erro ao Registrar:", e)
            return False

def historico_livros(id_usuario: str) -> bool:
    with SessionLocal() as session:
            try:
                livros_emprestados = session.query(Emprestimo).filter(Emprestimo.usuario_id == int(id_usuario)).all()

                if not livros_emprestados:
                    print("❌ Você você não pegou livros emprestado.")
                    return False

                for i in livros_emprestados:
                    status = "Não devolvido" if not i.data_devolucao else f"Devolvido em {i.data_devolucao}"
                    print(f"- {i.livro.titulo} | Data do emprestimo {i.data_emprestimo} | {status}" )
                    return True

            except Exception as e:
                session.rollback()
                print(f"Falha em listar livros empretado: {e}")
                return False

def editar_livro(id: int, titulo: str, autor: str, ano: int) -> bool:
    with SessionLocal() as session:
        try:
            livro = session.query(Livro).filter(Livro.id == id).first()

            livro.titulo = titulo
            livro.autor = autor
            livro.ano = ano

            session.commit()

            return True
        
        except Exception as e:
            session.rollback()
            print(f"Falha na edição: {e}")
            return False

def excluir_livro(id: int) -> bool:
    with SessionLocal() as session:
        try:
            livro = session.query(Livro).filter(Livro.id == id).first()

            if not livro:
                print("Nenhum livro corresponde a esse id.")

            session.delete(livro)
            session.commit()
            return True
        
        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir: {e}")
            return False