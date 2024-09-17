import base64
import logging
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None, sender_public_key=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature  # Assinatura da transação
        self.sender_public_key = sender_public_key  # Chave pública do remetente

    def to_string(self):
        return f"{self.sender}{self.recipient}{self.amount}"

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'signature': base64.b64encode(self.signature).decode('utf-8') if self.signature else None,
            'sender_public_key': self.sender_public_key,
        }

    @classmethod
    def from_dict(cls, tx_data):
        signature = base64.b64decode(
            tx_data['signature']) if tx_data['signature'] else None
        return cls(
            sender=tx_data['sender'],
            recipient=tx_data['recipient'],
            amount=tx_data['amount'],
            signature=signature,
            sender_public_key=tx_data['sender_public_key']
        )

    def sign_transaction(self, private_key):
        transaction_data = self.to_string().encode('utf-8')
        self.signature = private_key.sign(
            transaction_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return self.signature  # Certifique-se de retornar a assinatura

    def verify_signature(self):
        if not self.sender_public_key:
            logging.error("Falha na verificação: Chave pública ausente.")
            return False
        try:
            # Carrega a chave pública a partir do PEM fornecido
            public_key = serialization.load_pem_public_key(
                self.sender_public_key)

            # Verifica a assinatura
            public_key.verify(
                self.signature,
                self.to_string().encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            logging.error("Falha na verificação: Assinatura inválida.")
            return False
        except ValueError:
            logging.error("Falha na verificação: Chave pública inválida.")
            return False

    def __str__(self):
        return f"Transaction(sender={self.sender}, recipient={self.recipient}, amount={self.amount})"

    def __repr__(self):
        return self.__str__()

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
                salt BLOB,
                tag BLOB,
                ciphertext BLOB,
                FOREIGN KEY(block_index) REFERENCES blocks(block_index)
            )
        ''')
