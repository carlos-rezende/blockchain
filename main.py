from src.blockchain import Blockchain
from src.transaction import Transaction
from src.wallet import Wallet


def main():
    blockchain = Blockchain()

    # Adiciona alguns participantes
    # Alice tem uma participação inicial
    blockchain.stake_holders["Alice"] = 100
    blockchain.stake_holders["Bob"] = 50

    # Cria e adiciona uma transação
    transaction = Transaction(
        sender="Alice", recipient="Bob", amount=10, sender_public_key=None)
    blockchain.create_transaction(transaction)

    # Realiza a mineração (PoS)
    blockchain.mine_pending_transactions_pos()

    # Exibe os blocos na blockchain
    for block in blockchain.chain:
        print(f"Bloco #{
              block.index} - Transações: {[tx.__dict__ for tx in block.transactions]}")


if __name__ == "__main__":
    main()
