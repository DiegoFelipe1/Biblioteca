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

          