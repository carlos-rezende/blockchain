class Transaction:
    def __init__(self, sender, recipient, amount, signature=None, sender_public_key=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature  # Assinatura da transação
        self.sender_public_key = sender_public_key  # Chave pública do remetente

    def to_string(self):
        return f"{self.sender}{self.recipient}{self.amount}"
