class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender  # Remetente da transação
        self.recipient = recipient  # Destinatário da transação
        self.amount = amount  # Valor transferido
