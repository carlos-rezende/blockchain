from src.wallet import Wallet
from src.blockchain import Blockchain
from src.transaction import Transaction
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestMinerReward(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()

    def test_miner_reward(self):
        # Minerador inicializa com saldo zero
        miner_address = "Minerador1"
        initial_balance = self.blockchain.get_balance(miner_address)
        self.assertEqual(initial_balance, 0)

    # Adiciona uma transação inicial para garantir que a mineração possa ser realizada
        initial_transaction = Transaction(
            sender=None,  # Transação inicial para criar saldo
            recipient="Alice",
            amount=100
        )
        self.blockchain.create_transaction(initial_transaction)
        self.blockchain.mine_pending_transactions(miner_address)

    # Cria e minera um bloco
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)
        self.blockchain.create_transaction(transaction)
        self.blockchain.mine_pending_transactions(miner_address)

    # Verifica se a recompensa foi adicionada
        miner_balance = self.blockchain.get_balance(miner_address)
        self.assertEqual(miner_balance, self.blockchain.mining_reward)


if __name__ == '__main__':
    unittest.main()
