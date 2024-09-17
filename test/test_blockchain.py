from src.wallet import Wallet
from src.transaction import Transaction
from src.blockchain import Blockchain
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestBlockchain(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def test_insufficient_funds_transaction(self):
        # Tenta criar uma transação com fundos insuficientes
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=1000,  # Valor maior do que o saldo inicial
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)

        # Verifica se o saldo de "Alice" é zero
        self.assertEqual(self.blockchain.get_balance("Alice"), 0)

        # Verifica se a transação é inválida devido a saldo insuficiente
        self.assertFalse(self.blockchain.create_transaction(transaction))

    def test_mine_block(self):
        # Adiciona saldo inicial para "Alice" para permitir que ela faça a transação
        initial_transaction = Transaction(
            sender=None,  # Indica uma transação de criação de saldo
            recipient="Alice",
            amount=100,
        )
        self.blockchain.create_transaction(initial_transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Cria uma transação e minera um bloco
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)
        self.assertTrue(self.blockchain.create_transaction(transaction))

        # Minera o bloco com a nova transação
        self.blockchain.mine_pending_transactions("Minerador2")

        # Verifica se a blockchain agora possui três blocos (gênesis + 2 minerados)
        self.assertEqual(len(self.blockchain.chain), 3)


if __name__ == '__main__':
    unittest.main()
