import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, data, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = 0  # Para o algoritmo de prova de trabalho
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Hash inclui o índice, hash anterior, dados, timestamp e nonce
        block_string = f"{self.index}{self.previous_hash}{
            self.data}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Prova de trabalho: encontra um hash que começa com 'difficulty' zeros
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Bloco minerado: {self.hash}")
