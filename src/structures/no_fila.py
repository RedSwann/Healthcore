class NoFila:
    def __init__(self, paciente, nivel):
        self.paciente = paciente
        self.nivel = nivel
        self.tempo_espera = 0
        self.proximo = None
        self.pontuacao = 0