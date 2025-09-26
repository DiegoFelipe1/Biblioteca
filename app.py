from database import SessionLocal, Usuario, Livro, Emprestimo
from datetime import datetime
import bcrypt
import uuid

usuario_logado = None

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
            opcao_usuario()

# TODO: adicionar logs em vez de apenas prints

def listar_livros():
    with SessionLocal() as session:
        livros = session.query(Livro).all()
        if not livros:
            return False
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")
        
def cadastrar_novo_usuario():
    name = input("\nPor favor, digite o nome do usuario: ")
    email =input("\nPor favor, digite o seu email (exemplo: email@email.com): ")
    senha = input("\nPor favor, digite uma senha: ")
    role = input("Digite o cargo: ")

    with SessionLocal() as session:
        try:
            hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
            novo_usuario = Usuario(
                nome=name,
                email=email,
                senha=hashed.decode("utf-8"),
                role = role
            )
            session.add(novo_usuario)
            session.commit()
            print(f"\n✅ Usuario {name} foi criado com sucesso!!")
        except Exception as e:
            session.rollback()
            print("Erro ao Registrar:", e)

def login(email, password):
    global usuario_logado # Torna a variavel global

    with SessionLocal() as session:
        # Filtra no banco de dados por email
        usuario = session.query(Usuario).filter_by(email=email).first()
        # Faz a verificação se a senha que foi criptografada bate com o DB
        if usuario and bcrypt.checkpw(password.encode("utf-8"),
                                      usuario.senha.encode("utf-8")):
            token = str(uuid.uuid4())
            usuario_logado = {
                "id": usuario.id,
                "nome": usuario.nome,
                "role": usuario.role,
                "token": token
            }
            print(f"""4
🔓 Login realizado com sucesso!!
Seja bem vindo {usuario.nome}""")
            return True
        else:
            print("❌ Email ou senha incorretos.")
            return False

def logout():
    global usuario_logado
    usuario_logado = None
    print("\n Logout realizado com sucesso.")

def adicionar_novo_livro():
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

def opcao_usuario():
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

        with SessionLocal() as session:
            try:
                livro = session.query(Livro).filter(Livro.id == int(id_livro)).first()
                usuario = session.query(Usuario).filter(Usuario.id == int(id_usuario)).first()

                if not livro:
                    print("\n❌ Livro não encotrado.")
                elif not livro.disponivel:
                    print("\n❌ Livro já emprestrado.")
                elif not usuario:
                    print("\n❌ Usuario não encotrado.")
                else:
                    livro.disponivel = False

                    emprestimo = Emprestimo(
                        usuario_id = id_usuario,
                        livro_id = id_livro
                    )

                    session.add(emprestimo)
                    session.commit()
                    print(f"\n✅ Você pegou emprestado livro: {livro.titulo}")

            except Exception as e:
                session.rollback()
                print(f"\n❌ Erro ao tentar emprestaro livro: {e}")
            
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
        cadastrar_novo_usuario()

    elif opcao == '3':
        # ENCERRA O LOOP
        break

    else:
        print("Atenção! Você digitou uma opção invalida.")

if __name__ == "__main__":
    pass