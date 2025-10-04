from models.livro import Livro
from models.usuario import Usuario
from models.emprestimo import Emprestimo
from sqlalchemy.orm import joinedload
from database import SessionLocal
from datetime import datetime



def emprestar_livro(id_livro: str, id_usuario: str) -> bool:
    with SessionLocal() as session:
            try:
                livro = session.query(Livro).filter(Livro.id == int(id_livro)).first()
                usuario = session.query(Usuario).filter(Usuario.id == int(id_usuario)).first()

                if not livro:
                    print("\n❌ Livro não encotrado.")
                    return False
                
                elif not livro.disponivel:
                    print("\n❌ Livro já emprestrado.")
                    return False
                
                elif not usuario:
                    print("\n❌ Usuario não encotrado.")
                    return False
                
                else:
                    livro.disponivel = False

                    emprestimo = Emprestimo(
                        usuario_id = id_usuario,
                        livro_id = id_livro
                    )
                    session.add(emprestimo)
                    session.commit()
                    print(f"\n✅ Você pegou emprestado livro: {livro.titulo}")
                    return True

            except Exception as e:
                session.rollback()
                print(f"\n❌ Erro ao tentar emprestaro livro: {e}")
                return False

def devolver_livro(id_usuario: str, id_livro: str) -> bool:
       with SessionLocal() as session:
            try:
                livro_devolvido = session.query(Emprestimo).filter(
                    Emprestimo.usuario_id == int(id_usuario),
                    Emprestimo.livro_id == int(id_livro),
                    Emprestimo.data_devolucao.is_(None)).first()

                if not livro_devolvido:
                    return False

                else:
                    livro_devolvido.data_devolucao = datetime.now()
                    livro_devolvido.livro.disponivel = True
                    session.commit()
                    return True
                
            except Exception as e:
                session.rollback()
                print(f"❌ Erro ao devolver livro: {e}")
                return False

def listar_emprestimos(id_usuario: int = None) -> list[dict]:
     with SessionLocal() as session:
        try:
            # Cria a query base com eager loading de livro e usuário
            query = session.query(Emprestimo).options(
                joinedload(Emprestimo.livro),
                joinedload(Emprestimo.usuario)
            )

            # Se id_usuario for passado, filtra
            if id_usuario:
                query = query.filter(Emprestimo.usuario_id == id_usuario)

            emprestimos = query.all()

            if not emprestimos:
                 return []
            
            return [
                {
                    "id": e.id,
                    "titulo": e.livro.titulo,
                    "autor": e.livro.autor,
                    "ano": e.livro.ano,
                    "data_emprestimo": e.data_emprestimo,
                    "data_devolucao": e.data_devolucao
                }
                for e in emprestimos
            ]
        
        except Exception as e:
               session.rollback()
               print(f"Erro ao listar emprestimos: {e}")
               return []
        
