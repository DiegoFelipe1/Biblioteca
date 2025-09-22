from database import SessionLocal, Usuario, Livro, Emprestimo
from datetime import datetime


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

# TODO: adicionar logs em vez de apenas prints

def listar_livros():
    with SessionLocal() as session:
        livros = session.query(Livro).all()
        if not livros:
            print("📚 Não existe livros disponiveis.")   
        else:
            print("\n📚 Livros disponiveis:\n")
            for livro in livros:
                print(f"{livro.id}. {livro.titulo} || {livro.autor} || {livro.ano}")
        
def cadastrar_novo_usuario():
    name = input("\nPor favor digite o nome do usuario: ")
    email =input("\nPor favor digite o seu email (exemplo: email@email.com): ")

    with SessionLocal() as session:
        try:
            novo_usuario = Usuario(
                nome=name,
                contato=email
            )
            session.add(novo_usuario)
            session.commit()
            print(f"\n✅ Usuario {name} foi criado com sucesso!!")
        except Exception as e:
            session.rollback()
            print("Erro ao Registrar:", e)
        
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
4 - Voltar
''')
    opcao = input("\nPor favor digite um das opções acima: ")

    # Lista os livros e usuario pega emprestado   
    if opcao == "1":
        listar_livros()
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