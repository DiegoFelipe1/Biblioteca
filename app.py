from database import SessionLocal
from datetime import datetime
from service.emprestimo_service import emprestar_livro, devolver_livro
from service.usuario_service import login, usuario_logado, cadastrar_usuario, logout
from service.livro_service import listar_livros, historico_livros


'''
Usuario Seth:
    email: email@gmail.com
    senha: 123mudar
    role: user

Usuario Diego:
    email: diego@exemplo.com
    senha: mudar123    
'''

def msg_inicial():
        print('''
====================================================================
BEM VINDO A BIBLIOTECA:
              
1 - Login
2 - Criar uma conta
3 - Sair
''')

def menu_admin():
    pass

def menu_usuario():
    print('''
1 - Pegar livros
2 - Devolver livros
3 - Mostrar historico de livros
4 - Logout
''')
    opcao = input("\nPor favor digite um das opções acima: ")

    # Lista os livros e usuario pega emprestado   
    if opcao == "1":
        existem_livros = listar_livros()

        if not existem_livros:
            print("📚 Não existe livros disponiveis.")
            return msg_inicial()
    
        id_livro = input("\nPor favor, digite o numero de qual livro deseja pegar emprestrado: ")
        id_usuario = input("\nPor favor, digite o numero de seu ID: ")

        emprestar_livro(id_livro, id_usuario)
        
    elif opcao == "2":
        id_usuario = input("\nPor favor, digite o numero de seu ID: ")
        sucesso = devolver_livro(id_usuario)
        if not sucesso:
            print("Voltando ao menu...")

    elif opcao == "3":        
        id_usuario = input("\nPor favor, digite o numero de seu ID: ")
        historico_livros(id_usuario)

    elif opcao == "4":
        logout()
        return True

    else: 
        print("Atenção! Você digitou uma opção invalida.")
        return msg_inicial()
    
while True:

    msg_inicial()
    opcao = input("Por favor digite uma das opções acima: ")

    if opcao == '1':
        email = input("\nEmail: ")
        senha = input("\nSenha: ")
        
        usuario_logado = login(email, senha)
        if usuario_logado is not None:
            if usuario_logado["role"] == "admin":
                menu_admin()
            else:
                menu_usuario()

    elif opcao == '2':
        name = input("\nPor favor, digite o nome do usuario: ")
        email =input("\nPor favor, digite o seu email (exemplo: email@email.com): ")
        senha = input("\nPor favor, digite uma senha: ")
        role = input("Digite o cargo: ")
        cadastrar_usuario(name, email, senha, role)

    elif opcao == '3':
        # ENCERRA O LOOP
        break

    else:
        print("Atenção! Você digitou uma opção invalida.")

if __name__ == "__main__":
    pass