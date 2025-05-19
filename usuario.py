

class Usuario():
    def __init__(self, nome, contato):
        self.nome = nome
        self.contato = contato
        self.historico = []

    def pegar_livro(self, livro):
        if livro.emprestar():
            self.historico.append(livro)
            return f"O {livro.titulo} emprestado com sucesso!"
        
        else:
            return f"O {livro.titulo} não esta disponivel para emprestimos."


    def devolver_livro(self, livro):
        if livro in self.historico:
            self.historico.remove(livro)
            livro.devolver()
            return f"O livro {livro.titulo} foi devolvido com sucesso"
        else:
            return f"O livro {livro.titulo} não foi emprestado"

    def mostrar_historico(self):
        for i in self.historico:
            print(i)

        