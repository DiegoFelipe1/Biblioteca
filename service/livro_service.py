from models.livro import Livro
from models.usuario import Usuario
from models.emprestimo import Emprestimo
from database import SessionLocal

def listar_livros():
    with SessionLocal() as session:
        livros = session.query(Livro).all()
        if not livros:
            return False
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")

def adicionar_livro():
    titulo = input("\nDigite o titulo: ")
    autor = input("\nDigite o nome do autor: ")
    ano = int(input("\nDigite o ano do livro: "))

    with SessionLocal() as session:
        try:
            novo_livro = Livro(
                titulo=titulo,
                ano=ano, 
                autor=autor
            )
            session.add(novo_livro)
            session.commit()

            print(f"✅ O livro {titulo} foi adicionado com sucesso")

        except Exception as e:
            session.rollback()
            print("Erro ao Registrar:", e)

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
                print(f"Falha em listar livros empretado: {e}")
                return False