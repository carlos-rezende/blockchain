from src.wallet import Wallet
from src.blockchain import Blockchain
from src.transaction import Transaction
import unittest
import sys
import os
import time
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestPerformanceUnderLoad(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()

    def test_performance_under_load(self):
        # Define o número de transações e blocos a serem criados
        num_transactions = 1000
        num_blocks = 10

        start_time = time.time()

        # Cria transações e minera blocos
        for _ in range(num_blocks):
            for _ in range(num_transactions // num_blocks):
                transaction = Transaction(
                    sender="Alice",
                    recipient="Bob",
                    amount=1,
                    sender_public_key=self.wallet1.get_public_key()
                )
                transaction.signature = self.wallet1.sign_transaction(
                    transaction)
                self.blockchain.create_transaction(transaction)

            self.blockchain.mine_pending_transactions("Minerador1")

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Tempo para criar e minerar {num_blocks} blocos com {
              num_transactions} transações: {total_time:.2f} segundos")

        # Verifica se o número total de blocos é igual ao número de blocos minerados mais o bloco gênesis
        self.assertEqual(len(self.blockchain.chain), num_blocks + 1)

        # Opcional: Verifica se o tempo total de mineração está dentro de um limite aceitável (por exemplo, 120 segundos)
        self.assertLess(total_time, 120,
                        "Mineração demorou mais do que o esperado")


if __name__ == '__main__':
    unittest.main()
