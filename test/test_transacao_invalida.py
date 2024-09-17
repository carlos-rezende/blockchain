from src.wallet import Wallet
from src.blockchain import Blockchain
from src.transaction import Transaction
import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestInvalidTransaction(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()

    def test_invalid_transaction(self):
        # Teste transação com valor negativo
        invalid_transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=-50,
            sender_public_key=self.wallet1.get_public_key()
        )
        invalid_transaction.signature = self.wallet1.sign_transaction(
            invalid_transaction)

        self.assertFalse(
            self.blockchain.create_transaction(invalid_transaction))

        # Teste transação sem assinatura
        unsigned_transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )

        self.assertFalse(
            self.blockchain.verify_transaction(unsigned_transaction))


if __name__ == '__main__':
    unittest.main()
