import unittest
import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.transaction import Transaction
from src.blockchain import Blockchain
from src.wallet import Wallet

class TestMineBlockDifficulty(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def test_mine_block_difficulty(self):
        # Define diferentes níveis de dificuldade e mede o tempo de mineração
        for difficulty in range(1, 5):
            self.blockchain.difficulty = difficulty

            transaction = Transaction(
                sender="Alice",
                recipient="Bob",
                amount=50,
                sender_public_key=self.wallet1.get_public_key()
            )
            transaction.signature = self.wallet1.sign_transaction(transaction)
            self.blockchain.create_transaction(transaction)

            # Minera o bloco e mede o tempo
            start_time = time.time()
            self.blockchain.mine_pending_transactions("Minerador1")
            end_time = time.time()

            mining_time = end_time - start_time
            print(f"Mining block with difficulty {difficulty} took {mining_time:.2f} seconds")

            # Você pode adicionar uma asserção opcional para verificar se o tempo está dentro de um limite aceitável
            # Por exemplo, se a mineração não deve levar mais de 60 segundos para qualquer nível de dificuldade
            self.assertLess(mining_time, 60, f"Mining took too long for difficulty {difficulty}")

if __name__ == '__main__':
    unittest.main()
