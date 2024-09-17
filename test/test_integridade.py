from src.wallet import Wallet
from src.blockchain import Blockchain
from src.transaction import Transaction
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


class TestBlockchainIntegrity(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def test_blockchain_integrity(self):
        # Adiciona saldo inicial para "Alice" para permitir que ela faça a transação
        initial_transaction = Transaction(
            sender=None,  # Indica uma transação de criação de saldo
            recipient="Alice",
            amount=100,
        )
        self.blockchain.create_transaction(initial_transaction)
        self.blockchain.mine_pending_transactions("Minerador1")

        # Verifica o saldo de Alice após a mineração do bloco inicial
        self.assertEqual(self.blockchain.get_balance("Alice"), 100)

        # Cria e adiciona uma nova transação de "Alice" para "Bob"
        transaction = Transaction(
            sender="Alice",
            recipient="Bob",
            amount=50,
            sender_public_key=self.wallet1.get_public_key()
        )
        transaction.signature = self.wallet1.sign_transaction(transaction)

        # Adiciona a transação e minera um bloco
        self.assertTrue(self.blockchain.create_transaction(
            transaction))  # Garante que a transação foi aceita
        self.blockchain.mine_pending_transactions("Minerador2")

        # Verifica se a blockchain é válida após a mineração
        self.assertTrue(self.blockchain.is_chain_valid())

        # Verifica o saldo atualizado de Alice e Bob após a transação
        self.assertEqual(self.blockchain.get_balance("Alice"), 50)
        self.assertEqual(self.blockchain.get_balance("Bob"), 50)

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


if __name__ == '__main__':
    unittest.main()
