import hashlib
import time
from src.transaction import Transaction  # Importa a classe Transaction


class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions  # Lista de transações
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Serializa as transações como strings para incluí-las no hash
        transactions_str = ''.join(str(tx.__dict__)
                                   for tx in self.transactions)
        block_string = f"{self.index}{self.previous_hash}{
            transactions_str}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Bloco minerado: {self.hash}")

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash,
        }

    @classmethod
    def from_dict(cls, block_data):
        transactions = [Transaction.from_dict(
            tx_data) for tx_data in block_data['transactions']]
        block = cls(
            block_data['index'],
            block_data['previous_hash'],
            transactions,
            block_data['timestamp']
        )
        block.nonce = block_data['nonce']
        block.hash = block_data['hash']
        return block

    def __str__(self):
        return f"Block(index={self.index}, hash={self.hash}, transactions={self.transactions})"

    def __repr__(self):
        return self.__str__()
