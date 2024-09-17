import unittest
import json
from src.blockchain import Blockchain
from src.transaction import Transaction


class TestBlockchainCryptography(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()
        self.transaction_data = {
            'sender': 'Alice',
            'recipient': 'Bob',
            'amount': 50,
            'signature': 'fake_signature',
            'sender_public_key': 'fake_public_key'
        }

    def test_encrypt_decrypt_data(self):
      # Criptografa os dados da transação
        transaction_json = json.dumps(self.transaction_data).encode('utf-8')
        salt, nonce, tag, ciphertext = self.blockchain.encrypt_data(
            transaction_json, self.blockchain.encryption_password)

      # Descriptografa os dados
        decrypted_data = self.blockchain.decrypt_data(
            salt, nonce, tag, ciphertext, self.blockchain.encryption_password)

      # Verifica se os dados descriptografados são iguais aos dados originais
        decrypted_transaction = json.loads(decrypted_data)
        self.assertEqual(decrypted_transaction, self.transaction_data)


if __name__ == '__main__':
    unittest.main()
