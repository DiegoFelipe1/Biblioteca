import pytest
import bcrypt
from models import Usuario, Livro, Emprestimo
from service.usuario_service import cadastrar_usuario, login 
from database import SessionLocal, Base, engine

'''
.fixture é uma função especial que prepara algum recurso antes do teste começar

scope = "module" -> Define o escopo da fixture

function -> roda a cada teste
module -> roda uma vez por modulo (arquivo teste)
session -> roda uma vez para toda a sessão de teste

autouse=True Quer dizer que ela vai rodar automaticamente, sem precisar como parametro na função teste
'''

@pytest.fixture(scope="function", autouse=True)
def database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)     # Cria o DB
    yield                                   # Executa a bateria de teste
    Base.metadata.drop_all(bind=engine)       # Remove todas as tabelas do banco, limpando o ambiente de teste

@pytest.fixture
def usuario_exem():
    with SessionLocal() as session:
        senha_hash = bcrypt.hashpw("12345".encode("utf-8"), bcrypt.gensalt())
        user = Usuario(nome="Diego", email="email@gmail.com", senha=senha_hash.decode("utf-8"))
        session.add(user)
        session.commit()
        return user


def test_login_sucesso(usuario_exem):
    usuario = login("email@gmail.com", "12345")

    assert usuario is not None
    assert usuario["nome"] == "Diego"
    assert usuario["role"] == "user"

def test_login_falha(usuario_exem):
    usuario = login("naoexiste@email.com", "senhaerrada")
    assert usuario is False
