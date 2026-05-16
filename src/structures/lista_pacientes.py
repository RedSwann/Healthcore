import pandas as pd
import json
import os
from structures.no_paciente import NoPaciente


class ListaPacientes:

    def __init__(self):
        self.inicio = None
        self.arquivo = "data/pacientes.json"
        self.carregar_json()

    # =========================
    # CARREGAR JSON
    # =========================
    def carregar_json(self):

        if not os.path.exists(self.arquivo):
            return

        with open(self.arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        for p in dados:
            self._inserir_sem_salvar(
                p["nome"],
                p["cpf"],
                p["idade"],
                p["telefone"],
                p["deficiencia"]
            )

    # =========================
    # SALVAR JSON
    # =========================
    def salvar_json(self):

        dados = []
        atual = self.inicio

        while atual:
            dados.append({
                "nome": atual.nome,
                "cpf": atual.cpf,
                "idade": atual.idade,
                "telefone": atual.telefone,
                "deficiencia": atual.deficiencia
            })
            atual = atual.proximo

        os.makedirs("data", exist_ok=True)

        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # =========================
    # INSERÇÃO INTERNA (SEM SALVAR)
    # =========================
    def _inserir_sem_salvar(self, nome, cpf, idade, telefone, deficiencia):

        novo = NoPaciente(nome, cpf, idade, telefone, deficiencia)

        if not self.inicio:
            self.inicio = novo
            return

        atual = self.inicio
        while atual.proximo:
            atual = atual.proximo

        atual.proximo = novo

    # =========================
    # INSERIR PACIENTE
    # =========================
    def inserir(self, nome, cpf, idade, telefone, deficiencia):

        if self.buscar(cpf):
            return False

        self._inserir_sem_salvar(nome, cpf, idade, telefone, deficiencia)

        self.salvar_json()
        return True

    # =========================
    # BUSCAR
    # =========================
    def buscar(self, cpf):

        atual = self.inicio

        while atual:
            if atual.cpf == cpf:
                return atual
            atual = atual.proximo

        return None

    # =========================
    # REMOVER
    # =========================
    def remover(self, cpf):

        atual = self.inicio
        anterior = None

        while atual:

            if atual.cpf == cpf:

                if anterior:
                    anterior.proximo = atual.proximo
                else:
                    self.inicio = atual.proximo

                self.salvar_json()
                return True

            anterior = atual
            atual = atual.proximo

        return False

    # =========================
    # ATUALIZAR
    # =========================
    def atualizar(self, cpf, nome, idade, telefone, deficiencia):

        paciente = self.buscar(cpf)

        if paciente:
            paciente.nome = nome
            paciente.idade = idade
            paciente.telefone = telefone
            paciente.deficiencia = deficiencia

            self.salvar_json()
            return True

        return False

    # =========================
    # DATAFRAME
    # =========================
    def dataframe(self):

        dados = []
        atual = self.inicio

        while atual:
            dados.append({
                "Nome": atual.nome,
                "CPF": atual.cpf,
                "Idade": atual.idade,
                "Telefone": atual.telefone,
                "Portador de deficiência": atual.deficiencia
            })
            atual = atual.proximo

        return pd.DataFrame(dados)

    # =========================
    # ORDENAÇÃO POR NOME
    # =========================
    def ordenar_por_nome(self):

        if not self.inicio or not self.inicio.proximo:
            return

        atual = self.inicio
        lista_ordenada = None

        while atual:
            proximo = atual.proximo
            atual.proximo = None
            lista_ordenada = self._inserir_ordenado(lista_ordenada, atual)
            atual = proximo

        self.inicio = lista_ordenada

    def _inserir_ordenado(self, inicio, novo_no):

        if not inicio or novo_no.nome.lower() < inicio.nome.lower():
            novo_no.proximo = inicio
            return novo_no

        atual = inicio

        while atual.proximo and atual.proximo.nome.lower() < novo_no.nome.lower():
            atual = atual.proximo

        novo_no.proximo = atual.proximo
        atual.proximo = novo_no

        return inicio