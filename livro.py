class Livro:
    def __init__(self, titulo, autor, ano):
        if not titulo:
            raise ValueError("Titulo não pode ser vazio")
        if not autor:
            raise ValueError("Autor não pode ser vazio")
        if not isinstance(ano, int) or ano < 0:
            raise ValueError("Ano invalido")
        
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = True

    def emprestar(self):
        if self.disponivel:
            self.disponivel = False
            return True
        else:
            return False
    
    def devolver(self):
        self.disponivel = True
    
    def __str__(self):
        status = "Disponivel" if self.disponivel else "Emprestado"
        return f"{self.titulo} - {self.autor} {self.ano} [{status}]"