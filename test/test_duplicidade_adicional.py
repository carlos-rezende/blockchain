from src.blockchain import Blockchain
from src.transaction import Transaction
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestBlockchainAdditional(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()

    def test_duplicate_transactions(self):
        transaction = Transaction(sender='Alice', recipient='Bob', amount=50)
        self.blockchain.create_transaction(transaction)
        # Tenta adicionar a mesma transação novamente
        result = self.blockchain.create_transaction(transaction)
        self.assertFalse(
            result, "A blockchain deveria rejeitar transações duplicadas.")


if __name__ == '__main__':
    unittest.main()
