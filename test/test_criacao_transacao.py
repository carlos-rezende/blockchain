from src.wallet import Wallet
from src.blockchain import Blockchain
from src.transaction import Transaction
import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestCreateTransaction(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def test_create_transaction(self):
        # Adiciona saldo inicial para "Alice" para permitir que ela faça a transação
        initial_transaction = Transaction(
            sender=None,  # Indica uma transação de criação de saldo
            recipient="Alice",
            amount=100,
        )
        self.blockchain.create_transaction(initial_transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Cria e adiciona uma nova transação de "Alice" para "Bob"
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)

        # Verifica a validade da transação
        self.assertTrue(self.blockchain.verify_transaction(transaction))

        # Adiciona a transação e minera um bloco
        self.assertTrue(self.blockchain.create_transaction(transaction))
        self.blockchain.mine_pending_transactions("Minerador2")


if __name__ == '__main__':
    unittest.main()
