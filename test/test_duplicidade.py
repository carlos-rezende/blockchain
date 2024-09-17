from src.wallet import Wallet
from src.blockchain import Blockchain
from src.transaction import Transaction
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestDuplicateTransactions(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def test_duplicate_transactions(self):
        # Adiciona saldo inicial para "Alice"
        initial_transaction = Transaction(
            sender=None,  # Transação inicial para criar saldo
            recipient="Alice",
            amount=100
        )
        self.blockchain.create_transaction(initial_transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

    # Cria uma transação válida
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)

    # Adiciona a transação pela primeira vez
        self.assertTrue(self.blockchain.create_transaction(transaction))

    # Tenta adicionar a mesma transação novamente
        is_added = self.blockchain.create_transaction(transaction)

    # Verifica se a transação duplicada foi rejeitada
        self.assertFalse(is_added)


if __name__ == '__main__':
    unittest.main()
