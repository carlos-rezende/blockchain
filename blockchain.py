import random
import time
from block import Block
from transaction import Transaction
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []  # Lista de transações pendentes
        self.mining_reward = 100  # Recompensa pela mineração
        self.stake_holders = {}  # Armazena o saldo dos nós
        self.reputation = {}  # Armazena a reputação dos nós

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def create_transaction(self, transaction):
        # Verifica se o valor da transação é maior que zero
        if transaction.amount <= 0:
            print("Transação inválida: o valor deve ser maior que zero.")
            return False

        # Verifica se o remetente tem saldo suficiente
        if transaction.sender and self.get_balance(transaction.sender) < transaction.amount:
            print("Saldo insuficiente para a transação.")
            return False

        # Adiciona a transação pendente se for válida
        self.pending_transactions.append(transaction)
        return True

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

            # Verifica o hash do bloco
            if current_block.hash != current_block.calculate_hash():
                print(f"Hash do bloco #{current_block.index} está inválido.")
                return False

            # Verifica se o hash do bloco anterior está correto
            if current_block.previous_hash != previous_block.hash:
                print(f"Hash do bloco anterior do bloco #{
                      current_block.index} está inválido.")
                return False

            # Verifica todas as transações do bloco
            for transaction in current_block.transactions:
                if not self.verify_transaction(transaction):
                    print(f"Transação inválida no bloco #{
                          current_block.index}.")
                    return False

        return True

    def verify_transaction(self, transaction):
        # Ignora transações sem chave pública (como transações de mineração)
        if transaction.sender_public_key is None:
            return True

    # Verifica a assinatura da transação
        try:
            public_key = serialization.load_pem_public_key(
                transaction.sender_public_key)
            transaction_data = transaction.to_string().encode()
            public_key.verify(
                transaction.signature,
                transaction_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except (InvalidSignature, TypeError, ValueError):
            return False

    def select_stakeholder(self):
        total_stake = sum(self.stake_holders.values())
        total_reputation = sum(self.reputation.values())

        if total_stake == 0 or total_reputation == 0:
            return None

        # Combina a stake com a reputação
        combined_weights = {
            node: self.stake_holders[node] * self.reputation.get(node, 1) for node in self.stake_holders}
        pick = random.uniform(0, sum(combined_weights.values()))
        current = 0
        for stakeholder, weight in combined_weights.items():
            current += weight
            if current > pick:
                return stakeholder
        return None

    def update_reputation(self, node, increase=True):
        if node not in self.reputation:
            self.reputation[node] = 1
        if increase:
            self.reputation[node] += 1
        else:
            # A reputação não pode ser menor que 1
            self.reputation[node] = max(1, self.reputation[node] - 1)

    def mine_pending_transactions(self, mining_reward_address):
        print(f"Transações antes da mineração: {self.pending_transactions}")
    # Cria um novo bloco contendo as transações pendentes
        block = Block(len(self.chain), self.get_latest_block().hash,
                      self.pending_transactions)
        block.mine_block(self.difficulty)

    # Adiciona o bloco minerado à cadeia
        self.chain.append(block)
        print(f"Bloco minerado: {block.hash}, Transações: {
              block.transactions}")

    # Reseta as transações pendentes e adiciona a recompensa ao minerador
        self.pending_transactions = [Transaction(
            None, mining_reward_address, self.mining_reward)]

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        return balance

    def create_block_from_data(self, data):
        return Block(data['index'], data['previous_hash'], data['transactions'], data['timestamp'])
