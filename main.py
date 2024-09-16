from blockchain import Blockchain
from transaction import Transaction


def main():
    # Cria a blockchain
    blockchain = Blockchain()

    # Cria algumas transações
    blockchain.create_transaction(Transaction("Alice", "Bob", 50))
    blockchain.create_transaction(Transaction("Bob", "Charlie", 30))

    # Minera as transações
    print("Minerando transações...")
    blockchain.mine_pending_transactions("Minerador_1")

    # Mostra o saldo do minerador
    print(f"Saldo do minerador: {blockchain.pending_transactions[0].recipient} recebeu {
          blockchain.pending_transactions[0].amount}")

    # Adiciona mais transações
    blockchain.create_transaction(Transaction("Charlie", "Alice", 20))
    blockchain.create_transaction(Transaction("Alice", "Bob", 10))

    # Minera as novas transações
    print("Minerando transações...")
    blockchain.mine_pending_transactions("Minerador_2")

    # Exibe os blocos na blockchain
    for block in blockchain.chain:
        print(f"Bloco #{block.index} - Hash: {block.hash} - Transações: {
              [tx.__dict__ for tx in block.transactions]}")


if __name__ == "__main__":
    main()
