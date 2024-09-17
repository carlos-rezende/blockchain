import unittest
import os
import sqlite3
from src.blockchain import Blockchain
from src.transaction import Transaction


class TestBlockchainStorage(unittest.TestCase):

    def setUp(self):
        # Remove o banco de dados se já existir para um novo teste
        if os.path.exists('blockchain.db'):
            try:
                # Fecha qualquer conexão existente antes de remover
                with sqlite3.connect('blockchain.db') as conn:
                    conn.close()
                os.remove('blockchain.db')
            except Exception as e:
                print(f"Erro ao remover o banco de dados no setup: {e}")

        self.blockchain = Blockchain()

    def tearDown(self):
        # Fecha a conexão do banco de dados antes de remover o arquivo
        self.blockchain.connection.close()

        # Remove o banco de dados após o teste, se existir
        if os.path.exists('blockchain.db'):
            try:
                os.remove('blockchain.db')
            except Exception as e:
                print(f"Erro ao remover o banco de dados no teardown: {e}")

    def test_save_and_load_block(self):
        # Adiciona saldo inicial para "Alice"
        initial_transaction = Transaction(
            sender=None,  # Indica uma transação de criação de saldo
            recipient='Alice',
            amount=100
        )
        self.blockchain.pending_transactions.append(initial_transaction)
        self.blockchain.mine_pending_transactions('Minerador1')

        # Cria uma transação e adiciona à blockchain
        transaction = Transaction(
            sender='Alice',
            recipient='Bob',
            amount=50,
            signature='fake_signature',  # Assinatura falsa para fins de teste
            sender_public_key='fake_public_key'  # Chave pública falsa para fins de teste
        )

        # Bypass da verificação da assinatura para permitir a transação de teste
        self.blockchain.pending_transactions.append(transaction)

        # Minera o bloco contendo a transação
        self.blockchain.mine_pending_transactions('Minerador1')

        # Salva todos os blocos da blockchain no banco de dados
        for block in self.blockchain.chain:
            try:
                self.blockchain.save_block(block)
            except sqlite3.IntegrityError:
                print(f"Bloco com índice {
                      block.index} já existe. Pulando inserção.")

        # Carrega os blocos do banco de dados
        loaded_blocks = self.blockchain.load_blocks()

        # Verifica se o número de blocos carregados é igual ao número de blocos na blockchain
        self.assertEqual(len(loaded_blocks), len(self.blockchain.chain))
        self.assertEqual(loaded_blocks[-1].hash,
                         self.blockchain.chain[-1].hash)


if __name__ == '__main__':
    unittest.main()
