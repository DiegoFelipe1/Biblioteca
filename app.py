from database import SessionLocal
from datetime import datetime
from service.emprestimo_service import emprestar_livro, devolver_livro
from service.usuario_service import listar_usuarios, login, usuario_logado, cadastrar_usuario, logout
from service.livro_service import excluir_livro, editar_livro, adicionar_livro, listar_livros, historico_livros


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
    print('''
===============================
📚 Menu do Administrador
===============================
1 - Cadastrar livros
2 - Listar todos os livros
3 - Editar livro
4 - Remover livro
5 - Listar usuários
6 - Remover usuário
7 - Visualizar empréstimos
8 - Forçar devolução
9 - Cadastrar novo administrador
0 - Logout
''')
    opcao = input("\nPor favor digite um das opções acima: ")

    if opcao == "1":
        titulo = input("\nDigite o titulo: ")
        autor = input("\nDigite o nome do autor: ")
        ano = int(input("\nDigite o ano do livro: "))

        adicionar_livro(titulo, autor, ano)

        return menu_admin()
    
    elif opcao == "2":
        livros = listar_livros()

        if not livros:
            print("Não existe livros cadastrados.")
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")

        return menu_admin()
    
    elif opcao == "3":
        livros = listar_livros()

        if not livros:
            print("Não existe livros cadastrados.")
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")

        id = int(input("\nQual o id do livro que deseja editar? "))

        titulo = input("\nQual o novo titulo? ")
        autor = input("\nQual o novo nome do autor? ")
        ano = int(input("\nQual o novo ano? "))

        sucesso = editar_livro(id, titulo, autor, ano)

        if sucesso:
            print(f"✅ {titulo} foi editado com sucesso.")

        return menu_admin()
    
    elif opcao == "4":
        livros = listar_livros()

        if not livros:
            print("Não existe livros cadastrados.")
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")

        id = int(input("\nQual o id do livro que deseja remover? "))

        sucesso = excluir_livro(id)

        if sucesso:
            print("✅ Livro excluido com sucesso>")
        
        return menu_admin()
    
    elif opcao == "5":
        usuarios = listar_usuarios()

        if not usuarios:
            print("❌ Não existe usuarios no banco de dados.")

        else:
            for i in usuarios:
                print(f"{i.id} || {i.nome} || {i.email} || {i.role}")

        return menu_admin()
    
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