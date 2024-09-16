import time
from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []  # Lista de transações pendentes
        self.mining_reward = 100  # Recompensa pela mineração

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, mining_reward_address):
        # Cria um novo bloco contendo as transações pendentes
        block = Block(len(self.chain), self.get_latest_block().hash,
                      self.pending_transactions)
        block.mine_block(self.difficulty)

        # Adiciona o bloco minerado à cadeia
        self.chain.append(block)

        # Reseta as transações pendentes e adiciona a recompensa ao minerador
        self.pending_transactions = [Transaction(
            None, mining_reward_address, self.mining_reward)]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print("Hash do bloco atual está inválido")
                return False

            if current_block.previous_hash != previous_block.hash:
                print("Hash do bloco anterior está inválido")
                return False

        return True
