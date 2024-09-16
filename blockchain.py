import time
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Ajuste a dificuldade da mineração

    def create_genesis_block(self):
        # O bloco gênesis é o primeiro bloco da cadeia, criado manualmente
        return Block(0, "0", "Bloco Gênesis", time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Verifica a integridade da cadeia
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Recalcula o hash do bloco atual e compara
            if current_block.hash != current_block.calculate_hash():
                print("Hash do bloco atual está inválido")
                return False

            # Compara o hash do bloco anterior
            if current_block.previous_hash != previous_block.hash:
                print("Hash do bloco anterior está inválido")
                return False

        return True
