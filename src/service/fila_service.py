from datetime import datetime

from core.fila_atendimento import FilaAtendimento
from core.paciente import ListaPacientes
from core.pilha_acoes import Pilha


class FilaService:

    def __init__(self, lista, fila, historico):
        self.lista = lista
        self.fila = fila
        self.historico = historico

    # ======================
    # ADICIONAR NA FILA
    # ======================
    def adicionar(self, cpf, nivel):

        cpf = str(cpf).strip()

        if not cpf:
            return False, "Preencha o campo CPF."

        if not cpf.isdigit():
            return False, "CPF deve conter apenas números."

        if len(cpf) != 11:
            return False, "CPF deve conter exatamente 11 dígitos."

        paciente = self.lista.buscar(cpf)

        if not paciente:
            return False, "Paciente não cadastrado."

        ok = self.fila.adicionar(paciente, nivel)

        if not ok:
            return False, "Paciente já está na fila."

        self.historico.empilhar({
            "tipo": "adicionar_fila",
            "acao": "Entrada na fila",
            "cpf": paciente.cpf,
            "nome": paciente.nome,
            "nivel": nivel,
            "detalhes": f"Paciente {paciente.nome} entrou na fila com nível {nivel}.",
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

        return True, "Paciente adicionado."

    # ======================
    # ATENDER PRÓXIMO
    # ======================
    def atender(self):

        paciente_fila = self.fila.atender_proximo()

        if not paciente_fila:
            return False, "Fila vazia."

        paciente = paciente_fila.paciente

        self.historico.empilhar({
            "tipo": "atender",
            "acao": "Atendimento",
            "cpf": paciente.cpf,
            "nome": paciente.nome,
            "nivel": paciente_fila.nivel,
            "detalhes": f"Paciente {paciente.nome} foi atendido. Nível: {paciente_fila.nivel}.",
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

        return True, f"Atendendo {paciente.nome}"

    # ======================
    # DESFAZER ÚLTIMA AÇÃO
    # ======================
    def desfazer(self):

        acao = self.historico.desempilhar()

        if not acao:
            return False, "Nada para desfazer."

        tipo = acao.get("tipo")

        if tipo == "adicionar_fila":
            cpf = acao.get("cpf")

            if not cpf:
                return False, "Não foi possível desfazer: CPF não encontrado no histórico."

            removido = self.fila.remover(cpf)

            if not removido:
                return False, "Não foi possível desfazer: paciente não está mais na fila."

            return True, "Entrada na fila desfeita."

        if tipo == "atender":
            cpf = acao.get("cpf")
            nivel = acao.get("nivel")

            if not cpf or not nivel:
                return False, "Não foi possível desfazer: dados incompletos no histórico."

            paciente = self.lista.buscar(cpf)

            if not paciente:
                return False, "Não foi possível desfazer: paciente não está cadastrado."

            ok = self.fila.adicionar(paciente, nivel)

            if not ok:
                return False, "Não foi possível desfazer: paciente já está na fila."

            return True, "Atendimento desfeito. Paciente voltou para a fila."

        return False, "Esta ação do histórico não pode ser desfeita."
