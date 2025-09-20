'''
    LIVROS PARA TESTE:

"1984"  George Orwell, 1949

"Dom Casmurro"  Machado de Assis, 1899

"O Senhor dos Anéis"  J.R.R. Tolkien, 1954

"O Pequeno Príncipe"  Antoine de Saint-Exupéry, 1943

"A Revolução dos Bichos"  George Orwell, 1945


'''



class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []

    def adicionar_livros(self, livro):
        if livro not in self.livros:
            self.livros.append(livro)
            return f'\nO livro {livro.titulo} foi adicionado com sucesso.'
        else:
            return f"\nO livro {livro.titulo} já foi adicionado."
        
    def cadastrar_usuario(self, usuario):
        if usuario not in self.usuarios:
            self.usuarios.append(usuario)
            return f"\n✅ O usuario {usuario.nome} foi cadastrado com sucesso. "
        else:
            return f"\n❌ O usuario {usuario.nome} já existe."

    def listar_livros(self):
        print("\n 📚 Lista de livros:")
        for livros in self.livros:
            print(f'{livros}')

    def listar_usuarios(self):
        print("\n 👤 Lista de usuarios ativos:")
        for usuarios in self.usuarios:
            print(f"- {usuarios.nome}")

        