from src.wallet import Wallet
from src.transaction import Transaction
from src.blockchain import Blockchain
import unittest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestP2PSync(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()

    def test_p2p_sync(self):
        # Cria um blockchain simulado para representar o segundo nó
        blockchain_node2 = Blockchain()

        # Adiciona uma transação e minera um bloco no nó 1
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)
        self.blockchain.create_transaction(transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Mocka a resposta do segundo nó
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = [
                block.to_dict() for block in self.blockchain.chain
            ]

            # Sincroniza a blockchain do nó 2
            blockchain_node2.sync_chain(["http://localhost:5000"])

            # Verifica se o nó 2 possui a mesma cadeia que o nó 1
            self.assertEqual(len(blockchain_node2.chain),
                             len(self.blockchain.chain))


if __name__ == '__main__':
    unittest.main()
