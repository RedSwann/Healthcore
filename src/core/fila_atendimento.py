# 
ESCALA_URGENCIA = {
    "Vermelho": 100,
    "Laranja": 75,
    "Amarelo": 50,
    "Verde": 25
}

class NoFila:
    def __init__(self, paciente, nivel):
        self.paciente = paciente
        self.nivel = nivel
        self.tempo_espera = 0
        self.proximo = None
        self.pontuacao = 0

class FilaAtendimento:

    def __init__(self):
        self.inicio = None

    # =========================
    # ADICIONAR NA FILA
    # =========================
    def adicionar(self, paciente, nivel):

        # impede duplicação na fila
        if self.buscar(paciente.cpf):
            return False

        novo = NoFila(paciente, nivel)

        self._calcular_pontuacao(novo)

        self.inicio = self._inserir_ordenado(self.inicio, novo)

        return True

    # =========================
    # BUSCAR NA FILA
    # =========================
    def buscar(self, cpf):

        atual = self.inicio

        while atual:
            if atual.paciente.cpf == cpf:
                return atual
            atual = atual.proximo

        return None

    # =========================
    # ATENDER PRÓXIMO
    # =========================
    def atender_proximo(self):

        if not self.inicio:
            return None

        removido = self.inicio
        self.inicio = self.inicio.proximo

        # aumenta tempo dos outros pacientes
        self.atualizar_fila()

        return removido

    # =========================
    # ATUALIZA TEMPO DE ESPERA
    # =========================
    def atualizar_fila(self):

        atual = self.inicio

        while atual:
            atual.tempo_espera += 1
            self._calcular_pontuacao(atual)
            atual = atual.proximo

        self._reordenar()

    # =========================
    # CÁLCULO DE PONTUAÇÃO (URGÊNCIA)
    # =========================
    def _calcular_pontuacao(self, no):

        idade = no.paciente.idade
        deficiencia = 10 if no.paciente.deficiencia == "Sim" else 0
        tempo = no.tempo_espera

        no.pontuacao = (
            ESCALA_URGENCIA[no.nivel] * 0.5 +
            tempo * 0.25 +
            idade * 0.15 +
            deficiencia * 0.10
        )

    # =========================
    # INSERÇÃO ORDENADA
    # =========================
    def _inserir_ordenado(self, inicio, novo):

        if not inicio or novo.pontuacao > inicio.pontuacao:
            novo.proximo = inicio
            return novo

        atual = inicio

        while atual.proximo and atual.proximo.pontuacao >= novo.pontuacao:
            atual = atual.proximo

        novo.proximo = atual.proximo
        atual.proximo = novo

        return inicio

    # =========================
    # REORDENAÇÃO COMPLETA
    # =========================
    def _reordenar(self):

        atual = self.inicio
        nova = None

        while atual:
            prox = atual.proximo
            atual.proximo = None
            nova = self._inserir_ordenado(nova, atual)
            atual = prox

        self.inicio = nova

    # =========================
    # REMOVER DA FILA
    # =========================
    def remover(self, cpf):

        if not self.inicio:
            return False

        if self.inicio.paciente.cpf == cpf:
            self.inicio = self.inicio.proximo
            return True

        atual = self.inicio

        while atual.proximo:

            if atual.proximo.paciente.cpf == cpf:
                atual.proximo = atual.proximo.proximo
                return True

            atual = atual.proximo

        return False
