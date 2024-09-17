from src.wallet import Wallet
from src.blockchain import Blockchain
from src.transaction import Transaction
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestSignatureVerification(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()

    def test_signature_verification(self):
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)

        # Verifica se a assinatura é válida
        self.assertTrue(self.blockchain.verify_transaction(transaction))

        # Manipula a assinatura
        transaction.signature = b'invalid_signature'
        self.assertFalse(self.blockchain.verify_transaction(transaction))


if __name__ == '__main__':
    unittest.main()
