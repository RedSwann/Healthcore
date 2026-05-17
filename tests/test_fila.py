import unittest
from core.fila_atendimento import FilaAtendimento
from core.paciente import NoPaciente
import sys
sys.path.append("src")

class TestFilaAtendimento(unittest.TestCase):

    def criar_paciente(self, nome="Ana", cpf="1"):
        return NoPaciente(nome, cpf, 20, "9999", "Não")

    def test_adicionar_fila(self):
        fila = FilaAtendimento()

        p = self.criar_paciente()
        ok = fila.adicionar(p, "Amarelo")

        self.assertTrue(ok)
        self.assertIsNotNone(fila.inicio)

    def test_atender_vazio(self):
        fila = FilaAtendimento()
        self.assertIsNone(fila.atender_proximo())

    def test_ordem_basica(self):
        fila = FilaAtendimento()

        p1 = self.criar_paciente("Ana", "1")
        p2 = self.criar_paciente("Carlos", "2")

        fila.adicionar(p1, "Verde")
        fila.adicionar(p2, "Verde")

        atendido = fila.atender_proximo()

        self.assertIsNotNone(atendido)

if __name__ == "__main__":
    unittest.main()