class NoPaciente:
    def __init__(self, nome, cpf, idade, telefone, deficiencia):
        self.nome = nome
        self.cpf = cpf
        self.idade = idade
        self.telefone = telefone
        self.deficiencia = deficiencia
        self.proximo = None