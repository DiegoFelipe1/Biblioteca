from models.livro import Livro
from models.usuario import Usuario
from models.emprestimo import Emprestimo
from database import SessionLocal



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
  