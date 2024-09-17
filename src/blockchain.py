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
        # Deve ser armazenada em um local seguro
        self.encryption_password = b"super_secret_password"

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
                    encrypted_signature BLOB,
                    encrypted_sender_public_key BLOB,
                    nonce BLOB,
                    tag BLOB,
                    FOREIGN KEY(block_index) REFERENCES blocks(block_index)
                )
            ''')

            try:
                self.connection.execute(
                    'ALTER TABLE transactions ADD COLUMN encrypted_signature BLOB')
                self.connection.execute(
                    'ALTER TABLE transactions ADD COLUMN encrypted_sender_public_key BLOB')
                self.connection.execute(
                    'ALTER TABLE transactions ADD COLUMN nonce BLOB')
                self.connection.execute(
                    'ALTER TABLE transactions ADD COLUMN tag BLOB')
            except sqlite3.OperationalError:
                # Se as colunas já existirem, ignore o erro
                pass

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def create_transaction(self, transaction):
        # Permite transações de criação de saldo (sem remetente)
        if transaction.sender is None:
            self.pending_transactions.append(transaction)
            return True

        # Verifica se a chave pública está no formato correto (PEM e bytes)
        if isinstance(transaction.sender_public_key, str):
            transaction.sender_public_key = transaction.sender_public_key.encode(
                'utf-8')

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
                      self.pending_transactions, time.time())
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

        # Salva o bloco no banco de dados
        self.save_block(block)

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
            # Certifica-se de que a chave pública está no formato PEM e como bytes
            if isinstance(transaction.sender_public_key, str):
                transaction.sender_public_key = transaction.sender_public_key.encode(
                    'utf-8')

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
        except (InvalidSignature, ValueError) as e:
            print(
                f"Transação inválida: Assinatura inválida ou chave pública malformada. Erro: {e}")
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
        block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            self.pending_transactions,
            time.time()  # Adiciona o timestamp
        )
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

        # Gera um nonce para GCM
        nonce = os.urandom(12)

        # Criptografa os dados usando AES-GCM
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        return salt, nonce, encryptor.tag, ciphertext

    def decrypt_data(self, salt, nonce, tag, ciphertext, password):
        # Deriva a chave usando o mesmo KDF
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password)

        # Cria o decifrador com AES-GCM e o nonce
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def save_block(self, block):
        with self.connection:
            try:
                # Salva o bloco no banco de dados
                self.connection.execute('''
                INSERT INTO blocks (block_index, previous_hash, timestamp, nonce, hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (block.index, block.previous_hash, block.timestamp, block.nonce, block.hash))

                for transaction in block.transactions:
                    # Certifica-se de que a chave pública e assinatura são strings
                    sender_public_key = transaction.sender_public_key
                    signature = transaction.signature

                    # Verifica se a chave pública e a assinatura não são None
                    if sender_public_key and isinstance(sender_public_key, bytes):
                        sender_public_key = sender_public_key.decode('utf-8')

                    if signature and isinstance(signature, bytes):
                        signature = signature.decode('utf-8')

                    # Se a assinatura ou chave pública for None, define um valor padrão
                    if not sender_public_key:
                        sender_public_key = 'none'
                    if not signature:
                        signature = 'none'

                    # Criptografa a assinatura e a chave pública
                    _, nonce, tag, encrypted_signature = self.encrypt_data(
                        signature.encode('utf-8'), self.encryption_password)
                    _, _, _, encrypted_sender_public_key = self.encrypt_data(
                        sender_public_key.encode('utf-8'), self.encryption_password)

                    # Salva a transação no banco de dados
                    self.connection.execute('''
                    INSERT INTO transactions (block_index, sender, recipient, amount, encrypted_signature, encrypted_sender_public_key, nonce, tag)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (block.index, transaction.sender, transaction.recipient, transaction.amount, encrypted_signature, encrypted_sender_public_key, nonce, tag))
            except sqlite3.IntegrityError:
                print(f"Bloco com índice {
                      block.index} já existe. Pulando inserção.")

    def load_blocks(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM blocks ORDER BY block_index')
        blocks = []
        for row in cursor.fetchall():
            block_index, previous_hash, timestamp, nonce, hash_ = row
            # Carrega as transações relacionadas a esse bloco
            cursor.execute(
                'SELECT sender, recipient, amount, encrypted_signature, encrypted_sender_public_key, nonce, tag FROM transactions WHERE block_index=?', (block_index,))
            transactions = []
            for tx_row in cursor.fetchall():
                sender, recipient, amount, encrypted_signature, encrypted_sender_public_key, nonce, tag = tx_row

                # Descriptografa os dados
                try:
                    signature = self.decrypt_data(
                        nonce, nonce, tag, encrypted_signature, self.encryption_password).decode('utf-8')
                    sender_public_key = self.decrypt_data(
                        nonce, nonce, tag, encrypted_sender_public_key, self.encryption_password).decode('utf-8')

                    transactions.append(Transaction(
                        sender=sender,
                        recipient=recipient,
                        amount=amount,
                        signature=signature,
                        sender_public_key=sender_public_key
                    ))
                except Exception as e:
                    print(f"Erro ao descriptografar dados da transação: {e}")
                    continue

            blocks.append(Block(block_index, previous_hash,
                          transactions, timestamp, nonce, hash_))
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
