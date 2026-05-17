import unittest
from core.pilha_acoes import Pilha

class TestPilha(unittest.TestCase):

    def test_empilhar_e_desempilhar(self):
        pilha = Pilha()

        pilha.empilhar("acao1")
        pilha.empilhar("acao2")

        self.assertEqual(pilha.desempilhar(), "acao2")
        self.assertEqual(pilha.desempilhar(), "acao1")

    def test_pilha_vazia(self):
        pilha = Pilha()
        self.assertIsNone(pilha.desempilhar())

if __name__ == "__main__":
    unittest.main()