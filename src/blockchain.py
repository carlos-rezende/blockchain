import hashlib
import json
import logging
import os
import random
import time
import sqlite3
import requests
from src.block import Block
from src.transaction import Transaction
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []  # Lista de transações pendentes
        self.transaction_hashes = set()  # Armazena hashes das transações já processadas
        self.mining_reward = 100  # Recompensa pela mineração
        self.stake_holders = {}  # Armazena o saldo dos nós
        self.reputation = {}  # Armazena a reputação dos nós
        self.connection = sqlite3.connect('blockchain.db')
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS blocks (
                    block_index INTEGER PRIMARY KEY,
                    previous_hash TEXT,
                    timestamp REAL,
                    nonce INTEGER,
                    hash TEXT
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    block_index INTEGER,
                    sender TEXT,
                    recipient TEXT,
                    amount REAL,
                    signature TEXT,
                    sender_public_key TEXT,
                    FOREIGN KEY(block_index) REFERENCES blocks(block_index)
                )
            ''')

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def create_transaction(self, transaction):
        # Permite transações de criação de saldo (sem remetente)
        if transaction.sender is None:
            self.pending_transactions.append(transaction)
            return True

        # Verifica se o valor da transação é maior que zero
        if transaction.amount <= 0:
            print("Transação inválida: o valor deve ser maior que zero.")
            return False

        # Verifica a assinatura da transação
        if not self.verify_transaction(transaction):
            print("Transação inválida: Assinatura ausente ou inválida.")
            return False

        # Verifica saldo do remetente
        sender_balance = self.get_balance(transaction.sender)
        if sender_balance < transaction.amount:
            print("Saldo insuficiente para a transação.")
            return False

        # Verifica se a transação já foi incluída (evita duplicação)
        transaction_hash = transaction.to_string()
        if transaction_hash in self.transaction_hashes:
            print("Transação duplicada detectada.")
            return False

        # Adiciona a transação se for válida e não duplicada
        self.pending_transactions.append(transaction)
        self.transaction_hashes.add(transaction_hash)
        return True

    def mine_pending_transactions(self, mining_reward_address):
        # Cria um novo bloco contendo as transações pendentes
        block = Block(len(self.chain), self.get_latest_block().hash,
                      self.pending_transactions)
        block.mine_block(self.difficulty)

      # Processa as transações e atualiza os saldos
        for transaction in self.pending_transactions:
            if not self.verify_transaction(transaction):
                print(f"Transação inválida detectada e ignorada: {
                      transaction}")
            continue

        if transaction.sender:  # Exclui transações de criação de saldo inicial
            sender_balance = self.get_balance(transaction.sender)
            if sender_balance >= transaction.amount:
                # Deduz o valor do remetente
                self.stake_holders[transaction.sender] = sender_balance - \
                    transaction.amount
                # Adiciona o valor ao destinatário
                self.stake_holders[transaction.recipient] = self.get_balance(
                    transaction.recipient) + transaction.amount
            else:
                print(f"Saldo insuficiente para a transação de {
                      transaction.sender}.")
        else:
            # Transação de criação de saldo (gênesis)
            self.stake_holders[transaction.recipient] = self.get_balance(
                transaction.recipient) + transaction.amount

            # Adiciona o bloco minerado à cadeia
            self.chain.append(block)

            # Recompensa o minerador
            self.stake_holders[mining_reward_address] = self.get_balance(
                mining_reward_address) + self.mining_reward

            # Reseta as transações pendentes para incluir apenas a transação de recompensa ao minerador
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
        # Ignora a verificação de assinatura para transações de criação de saldo
        if transaction.sender is None:
            return True

        # Verifica se a transação tem uma assinatura e chave pública
        if not transaction.signature or not transaction.sender_public_key:
            print("Transação inválida: Assinatura ou chave pública ausente.")
            return False

        try:
            # Carrega a chave pública do remetente
            public_key = serialization.load_pem_public_key(
                transaction.sender_public_key)

            # Verifica a assinatura
            public_key.verify(
                transaction.signature,
                transaction.to_string().encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            print("Transação inválida: Assinatura inválida.")
            return False
        except Exception as e:
            print(f"Erro na verificação da transação: {e}")
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
        # Cria um novo bloco contendo as transações pendentes
        block = Block(len(self.chain), self.get_latest_block().hash,
                      self.pending_transactions)
        block.mine_block(self.difficulty)

        # Processa as transações e atualiza os saldos
        for transaction in self.pending_transactions:
            if transaction.sender:  # Exclui transações de criação de saldo inicial
                sender_balance = self.get_balance(transaction.sender)
                if sender_balance >= transaction.amount:
                    # Deduz o valor do remetente
                    self.stake_holders[transaction.sender] = sender_balance - \
                        transaction.amount
                    # Adiciona o valor ao destinatário
                    self.stake_holders[transaction.recipient] = self.get_balance(
                        transaction.recipient) + transaction.amount
                else:
                    print(f"Saldo insuficiente para a transação de {
                          transaction.sender}.")
            else:
                # Transação de criação de saldo (genesis)
                self.stake_holders[transaction.recipient] = self.get_balance(
                    transaction.recipient) + transaction.amount

        # Adiciona o bloco minerado à cadeia
        self.chain.append(block)

        # Recompensa o minerador
        self.stake_holders[mining_reward_address] = self.get_balance(
            mining_reward_address) + self.mining_reward

        # Reseta as transações pendentes para incluir apenas a transação de recompensa ao minerador
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

    def save_to_file(self, filename='blockchain.json'):
        with open(filename, 'w') as file:
            chain_data = [block.to_dict() for block in self.chain]
            json.dump(chain_data, file)

    def load_from_file(self, filename='blockchain.json'):
        try:
            with open(filename, 'r') as file:
                chain_data = json.load(file)
                self.chain = [Block.from_dict(block_data)
                              for block_data in chain_data]
        except (IOError, ValueError):
            print(
                "Erro ao carregar a blockchain do arquivo. Iniciando uma nova blockchain.")
            self.chain = [self.create_genesis_block()]

    def resolve_conflicts(self, peers):
        longest_chain = None
        max_length = len(self.chain)

        for peer in peers:
            try:
                response = requests.get(f'{peer}/chain')
                if response.status_code == 200:
                    peer_chain = response.json()
                    length = len(peer_chain)
                    print(f"Recebido peer chain de comprimento: {length}")

                    # Aceita a cadeia do peer se for mais longa ou do mesmo comprimento, mas válida
                    if (length > max_length or (length == max_length and longest_chain is None)) and self.is_valid_chain(peer_chain):
                        print(
                            "Encontrada uma cadeia mais longa ou válida de mesmo comprimento.")
                        max_length = length
                        longest_chain = peer_chain
            except requests.exceptions.RequestException as e:
                print(f"Erro ao conectar ao peer {peer}: {e}")
                continue

        # Substitui a cadeia local se encontrar uma cadeia mais longa ou válida
        if longest_chain:
            print("Substituindo a cadeia local com a nova cadeia válida.")
            self.chain = [Block.from_dict(block_data)
                          for block_data in longest_chain]
            return True
        print("Nenhuma cadeia mais longa ou válida encontrada.")
        return False

    def is_valid_chain(self, chain_data):
        temp_chain = [Block.from_dict(block_data) for block_data in chain_data]
        for i in range(1, len(temp_chain)):
            current_block = temp_chain[i]
            previous_block = temp_chain[i - 1]

            # Verifica se o hash do bloco atual está correto
            if current_block.hash != current_block.calculate_hash():
                print(f"Hash do bloco {current_block.index} inválido.")
                return False

            # Verifica se o hash do bloco anterior está correto
            if current_block.previous_hash != previous_block.hash:
                print(f"Hash do bloco anterior do bloco {
                      current_block.index} não corresponde.")
                return False

        return True

    def encrypt_data(self, data, password):
        # Deriva uma chave usando PBKDF2
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password)
        # Criptografa os dados usando AES
        cipher = Cipher(algorithms.AES(key), modes.GCM(os.urandom(12)))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return salt, cipher.algorithm, encryptor.tag, ciphertext

    def decrypt_data(self, salt, algorithm, tag, ciphertext, password):
        # Deriva a chave usando o mesmo KDF
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password)
        cipher = Cipher(algorithm, modes.GCM(tag))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def save_block(self, block):
        with self.connection:
            self.connection.execute('''
            INSERT INTO blocks (block_index, previous_hash, timestamp, nonce, hash)
            VALUES (?, ?, ?, ?, ?)
        ''', (block.index, block.previous_hash, block.timestamp, block.nonce, block.hash))

            for transaction in block.transactions:
                self.connection.execute('''
                    INSERT INTO transactions (block_index, sender, recipient, amount, signature, sender_public_key)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (block.index, transaction.sender, transaction.recipient, transaction.amount, transaction.signature, transaction.sender_public_key))

    def load_blocks(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM blocks ORDER BY index')
        blocks = []
        for row in cursor.fetchall():
            blocks.append(Block(*row))
        return blocks

    def sync_chain(self, nodes):
        for node in nodes:
            try:
                response = requests.get(f'{node}/chain')
                if response.status_code == 200:
                    external_chain = response.json()
                    if len(external_chain) > len(self.chain):
                        self.chain = [self.create_block_from_data(
                            block) for block in external_chain]
            except requests.exceptions.RequestException as e:
                print(f"Erro ao sincronizar com o nó {node}: {e}")
