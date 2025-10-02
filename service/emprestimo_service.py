from models.livro import Livro
from models.usuario import Usuario
from models.emprestimo import Emprestimo
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

def devolver_livro(id_usuario: str) -> bool:
       with SessionLocal() as session:
            try:
                livros_emprestados = session.query(Emprestimo).filter(
                    Emprestimo.usuario_id == int(id_usuario), 
                    Emprestimo.data_devolucao.is_(None)).all()

                if not livros_emprestados:
                    print("❌ Você não possui livros emprestado no momento!")
                    return False

                for i in livros_emprestados:
                    print(f"{i.livro_id} - {i.livro.titulo} || {i.livro.autor}")

                id_livro = input("\nPor favor, digite o numero do livro que irá devolver: ")

                livro_devolvido = session.query(Emprestimo).filter(
                    Emprestimo.usuario_id == int(id_usuario),
                    Emprestimo.livro_id == int(id_livro),
                    Emprestimo.data_devolucao.is_(None)).first()

                if not livro_devolvido:
                    print("❌ Este livro não foi emprestado pra você.")
                    return False

                else:
                    livro_devolvido.data_devolucao = datetime.now()
                    livro_devolvido.livro.disponivel = True
                    session.commit()
                    print(f"✅ O livro {livro_devolvido.livro.titulo} foi devolvido com sucesso!!")
                    return True
                
            except Exception as e:
                session.rollback()
                print(f"❌ Erro ao devolver livro: {e}")
                return False
