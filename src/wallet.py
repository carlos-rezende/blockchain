from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Wallet:
    def __init__(self):
        # Gera um par de chaves (pública e privada)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

    def sign_transaction(self, transaction):
        # Assina a transação com a chave privada
        transaction_data = f"{transaction.sender}{
            transaction.recipient}{transaction.amount}".encode()
        signature = self.private_key.sign(
            transaction_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return signature

    def get_public_key(self):
        # Retorna a chave pública em formato serializado
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
