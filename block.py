import hashlib
import time
from transaction import Transaction  # Importa a classe Transaction


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
