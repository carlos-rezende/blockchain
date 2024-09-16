import unittest
import os

from unittest.mock import patch
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet


class TestBlockchain(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def tearDown(self):
        # Remove o arquivo de persistência após os testes, se existir
        if os.path.exists('blockchain.json'):
            os.remove('blockchain.json')

    def test_create_transaction(self):
        # Adiciona saldo inicial para "Alice" para permitir que ela faça a transação
        initial_transaction = Transaction(
            sender=None,  # Indica uma transação de criação de saldo
            recipient="Alice",
            amount=100,
        )
        self.blockchain.create_transaction(initial_transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Cria uma nova transação válida a partir do saldo de "Alice"
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)

        # Verifica se a transação é válida
        self.assertTrue(self.blockchain.verify_transaction(transaction))

        # Adiciona a transação à blockchain
        self.assertTrue(self.blockchain.create_transaction(transaction))

    def test_insufficient_funds_transaction(self):
        # Tenta criar uma transação com fundos insuficientes
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=1000,  # Valor maior do que o saldo inicial
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)

        # Verifica se a transação é inválida devido a saldo insuficiente
        self.assertFalse(self.blockchain.create_transaction(transaction))

    def test_mine_block(self):
        # Cria uma transação e minera um bloco
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)
        self.blockchain.create_transaction(transaction)

        # Minera o bloco
        self.blockchain.mine_pending_transactions("Minerador1")

        # Verifica se a blockchain agora possui dois blocos (o bloco gênesis + o bloco minerado)
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_blockchain_integrity(self):
        # Adiciona saldo inicial para "Alice" para permitir que ela faça a transação
        initial_transaction = Transaction(
            sender=None,  # Indica uma transação de criação de saldo
            recipient="Alice",
            amount=100,
        )
        self.blockchain.create_transaction(initial_transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Cria e adiciona uma nova transação de "Alice" para "Bob"
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)
        self.blockchain.create_transaction(transaction)

        # Minera o bloco contendo a nova transação
        self.blockchain.mine_pending_transactions("Minerador2")

        # Verifica se a blockchain é válida após a mineração
        self.assertTrue(self.blockchain.is_chain_valid())

        # Certifica-se de que o bloco minerado contém pelo menos uma transação
        if len(self.blockchain.chain) > 1 and len(self.blockchain.chain[1].transactions) > 0:
            # Manipula a transação para testar a integridade
            self.blockchain.chain[1].transactions[0].amount = 1000
        else:
            # Failsafe - O teste falha se não encontrar transações no bloco
            self.fail(
                "Não foi possível configurar o teste - transação não encontrada no bloco.")

        # Verifica que a blockchain agora é inválida
        self.assertFalse(self.blockchain.is_chain_valid())

    def test_persistence(self):
        # Adiciona uma transação e minera um bloco
        transaction = Transaction(
            sender=None,
            recipient="Alice",
            amount=100
        )
        self.blockchain.create_transaction(transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Salva o estado da blockchain
        self.blockchain.save_to_file()

        # Cria uma nova instância da blockchain e carrega o estado do arquivo
        new_blockchain = Blockchain()
        new_blockchain.load_from_file()

        # Verifica se o novo estado carregado está correto
        self.assertEqual(len(new_blockchain.chain), len(self.blockchain.chain))
        self.assertTrue(new_blockchain.is_chain_valid())

    @patch('requests.get')
    def test_resolve_conflicts(self, mock_get):
        # Configura uma segunda blockchain para simular um nó diferente
        blockchain2 = Blockchain()

    # Adiciona uma transação e minera um bloco na blockchain original
        transaction = Transaction(
            sender=None,
            recipient="Alice",
            amount=100
        )
        self.blockchain.create_transaction(transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

    # Cria uma cadeia mais curta para o segundo nó
        blockchain2.create_transaction(transaction)
        blockchain2.mine_pending_transactions("Minerador2")

    # Simula a resposta HTTP para o peer, retornando a cadeia mais longa
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            block.to_dict() for block in self.blockchain.chain]

    # Simula a resolução de conflitos
        resolved = blockchain2.resolve_conflicts(["http://fake-peer"])
        print(f"Resolução de conflitos bem-sucedida: {resolved}")
        print(f"Comprimento da cadeia do blockchain2: {
              len(blockchain2.chain)}")
        print(f"Comprimento da cadeia do blockchain original: {
              len(self.blockchain.chain)}")

    # Verifica se a blockchain2 agora possui a cadeia mais longa
        self.assertTrue(resolved)
        self.assertEqual(len(blockchain2.chain), len(self.blockchain.chain))

    def test_synchronization(self):
        # Configura uma lista de peers e simula uma cadeia sincronizada
        peers = ["http://localhost:5001", "http://localhost:5002"]

        # Adiciona uma transação e minera um bloco
        transaction = Transaction(
            sender=None,
            recipient="Alice",
            amount=100
        )
        self.blockchain.create_transaction(transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Realiza uma sincronização simulada (não real, pois não há servidor)
        # Você pode substituir isso por uma chamada real de requests.get em um cenário real.
        for peer in peers:
            # Simula que os peers têm a cadeia atualizada
            peer_blockchain = Blockchain()
            peer_blockchain.chain = self.blockchain.chain.copy()
            self.assertTrue(peer_blockchain.is_chain_valid())
            self.assertEqual(len(peer_blockchain.chain),
                             len(self.blockchain.chain))


if __name__ == '__main__':
    unittest.main()
