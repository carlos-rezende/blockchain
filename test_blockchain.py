import unittest
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet


class TestBlockchain(unittest.TestCase):

    def setUp(self):
        # Configuração antes de cada teste
        self.blockchain = Blockchain()
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

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


if __name__ == '__main__':
    unittest.main()
