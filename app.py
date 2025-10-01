from database import SessionLocal
from datetime import datetime
from service.emprestimo_service import emprestar_livro
from service.usuario_service import login, usuario_logado, cadastrar_usuario
from service.livro_service import listar_livros

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
    if usuario_logado is None:
        print('''
====================================================================
BEM VINDO A BIBLIOTECA:
              
1 - Login
2 - Criar uma conta
3 - Sair
''')
    else:
        print(f"\n Usuario: {usuario_logado['nome']}")
        if usuario_logado["role"] == "admin":
            print("1 - Cadastrar livros\n2 - Listar usuários\n3 - Logout")
        else:
            menu_usuario()

def logout():
    global usuario_logado
    usuario_logado = None
    print("\n Logout realizado com sucesso.")

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
        listar_livros()

        if not listar_livros():
            print("📚 Não existe livros disponiveis.")
            return msg_inicial()
    
        id_livro = input("\nPor favor, digite o numero de qual livro deseja pegar emprestrado: ")
        id_usuario = input("\nPor favor, digite o numero de seu ID: ")

        emprestar_livro(id_livro, id_usuario)
        
    elif opcao == "2":
        id_usuario = input("\nPor favor, digite o numero de seu ID: ")

        with SessionLocal() as session:
            try:
                livros_emprestados = session.query(Emprestimo).filter(
                    Emprestimo.usuario_id == int(id_usuario), 
                    Emprestimo.data_devolucao.is_(None)).all()

                if not livros_emprestados:
                    print("❌ Você não possui livros emprestado no momento!")
                    return msg_inicial()

                for i in livros_emprestados:
                    print(f"{i.livro_id} - {i.livro.titulo} || {i.livro.autor}")

                id_livro = input("\nPor favor, digite o numero do livro que irá devolver: ")

                livro_devolvido = session.query(Emprestimo).filter(
                    Emprestimo.usuario_id == int(id_usuario),
                    Emprestimo.livro_id == int(id_livro),
                    Emprestimo.data_devolucao.is_(None)).first()

                if not livro_devolvido:
                    print("❌ Este livro não foi emprestado pra você.")

                else:
                    livro_devolvido.data_devolucao = datetime.now()
                    livro_devolvido.livro.disponivel = True
                    session.commit()
                    print(f"✅ O livro {livro_devolvido.livro.titulo} foi devolvido com sucesso!!")
            
            except Exception as e:
                session.rollback()
                print(f"❌ Erro ao devolver livro: {e}")

    elif opcao == "3":        
        id_usuario = input("\nPor favor, digite o numero de seu ID: ")

        with SessionLocal() as session:
            try:
                livros_emprestados = session.query(Emprestimo).filter(Emprestimo.usuario_id == int(id_usuario)).all()

                if not livros_emprestados:
                    print("❌ Você você não pegou livros emprestado.")
                    return msg_inicial()

                for i in livros_emprestados:
                    status = "Não devolvido" if not i.data_devolucao else f"Devolvido em {i.data_devolucao}"
                    print(f"- {i.livro.titulo} | Data do emprestimo {i.data_emprestimo} | {status}" )

            except Exception as e:
                print(f"Falha em listar livros empretado: {e}")

    elif opcao == "4":
        logout()
        msg_inicial()

    else: 
        print("Atenção! Você digitou uma opção invalida.")
        return msg_inicial()
    
while True:

    msg_inicial()
    opcao = input("Por favor digite uma das opções acima: ")

    if opcao == '1':
        email = input("\nEmail: ")
        senha = input("\nSenha: ")
        login(email, senha)

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