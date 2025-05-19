from livro import Livro
from usuario import Usuario
from biblioteca import Biblioteca

bib = Biblioteca()

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

def listar_livros(bib):
    lista = bib.listar_livros()
    return lista

def pegar_livro(bib):
    listar_livros()

def cadastrar_novo_usuario(bib):
    nome = input("\nPor favor digite o nome do usuario: ")
    contato =input("\nPor favor digite o seu email (exemplo: email@email.com): ")

    novo_usuario = Usuario(nome, contato)

    msg = bib.cadastrar_usuario(novo_usuario)

    return msg
    
def adicionar_novo_livro(bib):
    titulo = input("\nDigite o titulo: ")
    autor = input("\nDigite o nome do autor: ")
    ano = int(input("\nDigite o ano do livro: "))

    novo_livro = Livro(titulo, autor, ano)

    msg = bib.adicionar_livros(novo_livro)

    return msg

def opcao_usuario():
    print('''
1 - Pegar livros
2 - Devolver livros
3 - Mostrar historico de livros
4 - Voltar
''')
    opcao = input("\nPor favor digite um das opções acima:")
    
    if opcao == "1":
        lista = bib.listar_livros()
        print(lista)
    
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
        print(cadastrar_novo_usuario(bib))
        

    elif opcao == '2':
        print(adicionar_novo_livro(bib))
        
        
    elif opcao == '3':
        opcao_usuario(bib)

    elif opcao == '4':
        # CHAMA OPÇÕES DA BIBLIOTECA ????????
        pass

    else:
        # ENCERRA O LOOP
        break

if __name__ == "__main__":
    pass