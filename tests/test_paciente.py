import unittest
from core.paciente import ListaPacientes

class TestPaciente(unittest.TestCase):

    def setUp(self):
        self.lista = ListaPacientes()
        self.lista.inicio = None  # limpa lista em memória

    def test_inserir_paciente(self):
        ok = self.lista.inserir("Ana", "12345678901", 20, "9999", "Não")
        self.assertTrue(ok)

    def test_buscar_paciente(self):
        self.lista.inserir("Ana", "12345678901", 20, "9999", "Não")
        paciente = self.lista.buscar("12345678901")
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.nome, "Ana")

    def test_remover_paciente(self):
        self.lista.inserir("Ana", "12345678901", 20, "9999", "Não")
        ok = self.lista.remover("12345678901")
        self.assertTrue(ok)
        self.assertIsNone(self.lista.buscar("12345678901"))

if __name__ == "__main__":
    unittest.main()