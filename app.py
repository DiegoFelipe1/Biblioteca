from database import SessionLocal
from datetime import datetime
from service.emprestimo_service import listar_emprestimos, emprestar_livro, devolver_livro
from service.usuario_service import excluir_usuario, listar_usuarios, login, usuario_logado, cadastrar_usuario, logout
from service.livro_service import excluir_livro, editar_livro, adicionar_livro, listar_livros, historico_livros

# TODO: ajustar pegar livros (não esta colocando livro indisponivel no DB)
# TODO: erro ao mostrar historico de livros do usuario

'''
Usuario Seth:
    email: email@gmail.com
    senha: 123mudar
    role: user

Usuario Diego:
    email: diego@exemplo.com
    senha: mudar123    
    role: admin
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
8 - Cadastrar novo administrador
0 - Logout
''')
    opcao = input("\nPor favor digite um das opções acima: ")

    # Cadastrar livros
    if opcao == "1":
        titulo = input("\nDigite o titulo: ")
        autor = input("\nDigite o nome do autor: ")
        ano = int(input("\nDigite o ano do livro: "))

        adicionar_livro(titulo, autor, ano)

        return menu_admin()
    
    #Listar todos os livros
    elif opcao == "2":
        livros = listar_livros()

        if not livros:
            print("Não existe livros cadastrados.")
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")

        return menu_admin()
    
    # Editar livro
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
    
    # Remover livro
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
    
    # Listar usuários
    elif opcao == "5":
        usuarios = listar_usuarios()

        if not usuarios:
            print("❌ Não existe usuarios no banco de dados.")

        else:
            for i in usuarios:
                print(f"{i.id} || {i.nome} || {i.email} || {i.role}")

        return menu_admin()
    
    # Remover usuário
    elif opcao == "6":
        usuarios = listar_usuarios()

        if not usuarios:
            print("❌ Não existe usuarios no banco de dados.")
        else:
            for i in usuarios:
                print(f"{i.id} || {i.nome} || {i.email} || {i.role}")

        usuario_id = int(input("Por favor digite o id do usuario que deseja deletar: "))

        sucesso = excluir_usuario(usuario_id)

        if sucesso:
            print("\n✅ Usuario foi excluido com sucesso.")

        return menu_admin()

    # Visualizar empréstimos
    elif opcao == "7":
        emprestimos = listar_emprestimos()

        if not emprestimos:
            print("\nNenhum livro foi emprestado.")

        for i in emprestimos:
                devolucao = i.data_devolucao if i.data_devolucao else "Não devolvido"
                
                print(f'{i.usuario.nome} - {i.livro.titulo} || {i.data_emprestimo} || {devolucao}')
        
        return menu_admin()

    # Cadastrar novo administrador
    elif opcao == "8":
        name = input("\nPor favor, digite o nome do usuario: ")
        email =input("\nPor favor, digite o seu email (exemplo: email@email.com): ")
        senha = input("\nPor favor, digite uma senha: ")
        cadastrar_usuario(name, email, senha, role="admin")

        listar_usuarios()

        return menu_admin()
    
    # Logout
    elif opcao == "0":
        logout()
        return msg_inicial()
    
    # Mensagem caso não selecionar nenhuma das anteriores
    else:
        print("Atenção! Você digitou uma opção invalida.")
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
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in existem_livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")
    
        id_livro = input("\nPor favor, digite o numero de qual livro deseja pegar emprestrado: ")
        id_usuario = usuario_logado["id"]

        emprestar_livro(id_livro, id_usuario)
        
        return menu_usuario()
    
    # Devolver livros
    elif opcao == "2":
        # Verifica quais livros ele pegou emprestado
        id_usuario = usuario_logado["id"]
        emprestimos = listar_emprestimos(id_usuario)

        if not emprestimos:
            print("\nVocê não possui livros emprestados.")
            return menu_usuario()

        print("\n📚 Seus emprestimos:\n")
        for emprestimo in emprestimos:
            devolucao = emprestimo.data_devolucao if emprestimo.data_devolucao else "Não devolvido"

            print(f"{emprestimo.livro.id}. {emprestimo.livro.titulo} || {emprestimo.livro.autor} || {emprestimo.livro.ano} {devolucao}")
        
        # Faz a validação qual livro ele quer devolver
        id_livro = input("\nPor favor, digite o numero do livro que deseja devolver: ")
        sucesso = devolver_livro(id_usuario, id_livro)

        if not sucesso:
            print("\nErro ao devolver livro")
        else:
            print("\n✅ Livro devolvido com sucesso.")

        return menu_usuario()
    
    # Mostrar historico de livros
    elif opcao == "3":        
        id_usuario = usuario_logado["id"]
        historico = historico_livros(id_usuario)

        if not historico:
            print("❌ Você você não pegou livros emprestado.")
            
        for i in historico:
            status = "Não devolvido" if not i.data_devolucao else f"Devolvido em {i.data_devolucao}"
            
            print(f"- {i.livro.titulo} | Data do emprestimo {i.data_emprestimo} | {status}" )

        return menu_usuario()

    # Logout
    elif opcao == "4":
        logout()
        return msg_inicial()

    # Mensagem caso não selecionar nenhuma das anteriores
    else: 
        print("Atenção! Você digitou uma opção invalida.")
        return menu_usuario()
    
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
        cadastrar_usuario(name, email, senha, role="user")

    elif opcao == '3':
        # ENCERRA O LOOP
        break

    else:
        print("Atenção! Você digitou uma opção invalida.")

if __name__ == "__main__":
    pass