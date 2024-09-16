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
            'signature': self.signature,
            'sender_public_key': self.sender_public_key,
        }

    @classmethod
    def from_dict(cls, tx_data):
        return cls(
            sender=tx_data['sender'],
            recipient=tx_data['recipient'],
            amount=tx_data['amount'],
            signature=tx_data['signature'],
            sender_public_key=tx_data['sender_public_key']
        )
