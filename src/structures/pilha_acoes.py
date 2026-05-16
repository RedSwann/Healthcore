class PilhaAcoes:

    def __init__(self):
        self.itens = []

    def empilhar(self, acao):
        self.itens.append(acao)

    def desempilhar(self):
        if not self.itens:
            return None
        return self.itens.pop()