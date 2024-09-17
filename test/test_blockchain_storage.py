import unittest
import os
import sqlite3
from src.blockchain import Blockchain
from src.transaction import Transaction


class TestBlockchainStorage(unittest.TestCase):

    def setUp(self):
        # Fecha a conexão e remove o banco de dados se já existir para um novo teste
        if os.path.exists('blockchain.db'):
            try:
                # Fecha a conexão se estiver aberta
                self.blockchain = Blockchain()
                self.blockchain.connection.close()
            except Exception as e:
                print(f"Erro ao fechar conexão existente: {e}")

            try:
                os.remove('blockchain.db')
            except Exception as e:
                print(f"Erro ao remover o banco de dados no setup: {e}")

        # Cria uma nova instância do Blockchain para o teste
        self.blockchain = Blockchain()

    def tearDown(self):
        # Fecha a conexão do banco de dados após o teste
        self.blockchain.connection.close()

        # Remove o banco de dados após o teste
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

    # Cria uma transação com dados válidos para teste
        transaction = Transaction(
            sender='Alice',
            recipient='Bob',
            amount=50,
            signature='valid_signature',  # Assinatura fictícia para o teste
            # Chave pública fictícia para o teste
            sender_public_key='-----BEGIN PUBLIC KEY-----\nvalid_public_key...\n-----END PUBLIC KEY-----'
        )

        # Bypass da verificação da assinatura para permitir a transação de teste
        self.blockchain.pending_transactions.append(transaction)

        # Minera o bloco contendo a transação
        self.blockchain.mine_pending_transactions('Minerador1')

        # Salva todos os blocos da blockchain no banco de dados
        for block in self.blockchain.chain:
            try:
                print(f"Salvando bloco {block.index} no banco de dados.")
                self.blockchain.save_block(block)
            except sqlite3.IntegrityError:
                print(f"Bloco com índice {
                      block.index} já existe. Pulando inserção.")

            # Carrega os blocos do banco de dados
            loaded_blocks = self.blockchain.load_blocks()

            # Verifica se 'loaded_blocks' foi carregado corretamente
            print(f"Número de blocos na blockchain original: {
                  len(self.blockchain.chain)}")
            print(f"Número de blocos carregados do banco de dados: {
                  len(loaded_blocks)}")
        for i, block in enumerate(loaded_blocks):
            print(f"Bloco carregado [{i}] hash: {block.hash}")

            # Verifica se o número de blocos carregados é igual ao número de blocos na blockchain
            self.assertEqual(len(loaded_blocks), len(self.blockchain.chain))
            self.assertEqual(
                loaded_blocks[-1].hash, self.blockchain.chain[-1].hash)


if __name__ == '__main__':
    unittest.main()
