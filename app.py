from livro import Livro
from usuario import Usuario
from biblioteca import Biblioteca
from database import get_session, Usuario, Livro

bib = Biblioteca()

session = next(get_session())

def msg_inicial():
    print('''
====================================================================
BEM VINDO A BIBLIOTECA:

1 - Cadastrar usuario
2 - Adicionar livro
3 - Opções do usuario
4 - Opções da biblioteca
5 - Sair
''')

# TODO: implementar a função para listar livros disponíveis
# TODO: criar tratamento de erro para conexões com o banco
# TODO: adicionar logs em vez de apenas prints


def listar_livros():
    try:
        livros = session.query(Livro).all
        if not livros:
            print("📚 Não existe livros disponiveis.")
            
        else:
            print("📚 Livros disponiveis:")
            for livro in livros:
                print(f"{livro.titulo} || {livro.autor} || {livro.ano}")
        
    finally:
        session.close()

def cadastrar_novo_usuario():
    name = input("\nPor favor digite o nome do usuario: ")
    email =input("\nPor favor digite o seu email (exemplo: email@email.com): ")

    try:
        novo_usuario = Usuario(
            nome=name,
            contato=email
        )

        session.add(novo_usuario)
        session.commit()
        print(f"✅ Usuario {name} foi criado com sucesso!!")
    except Exception as e:
        session.rollback()
        print("Erro ao Registrar:", e)
    
    finally:
        session.close()

def adicionar_novo_livro():
    titulo = input("\nDigite o titulo: ")
    autor = input("\nDigite o nome do autor: ")
    ano = int(input("\nDigite o ano do livro: "))

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

    finally:
        session.close()

def opcao_usuario():
    print('''
1 - Pegar livros
2 - Devolver livros
3 - Mostrar historico de livros
4 - Voltar
''')
    opcao = input("\nPor favor digite um das opções acima:")
    
    if opcao == "1":
        pass
    elif opcao == "2":
        # CHAMA DEVOLVER LIVRO
        pass

    elif opcao == "3":
        # CHAMA HISTORICO
        pass

    else: 
        msg_inicial()
    
while True:

    msg_inicial()
    opcao = input("Por favor digite uma das opções acima: ")

    if opcao == '1':
        cadastrar_novo_usuario()
        

    elif opcao == '2':
        adicionar_novo_livro()
        
        
    elif opcao == '3':
        opcao_usuario()

    elif opcao == '4':
        # CHAMA OPÇÕES DA BIBLIOTECA ????????
        pass

    else:
        # ENCERRA O LOOP
        break

if __name__ == "__main__":
    pass