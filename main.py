from blockchain import Blockchain
from block import Block


def main():
    # Cria a blockchain
    blockchain = Blockchain()

    # Adiciona blocos à blockchain
    print("Minerando bloco 1...")
    blockchain.add_block(Block(1, "", "Bloco 1 Dados"))

    print("Minerando bloco 2...")
    blockchain.add_block(Block(2, "", "Bloco 2 Dados"))

    print("Minerando bloco 3...")
    blockchain.add_block(Block(3, "", "Bloco 3 Dados"))

    # Verifica a integridade da blockchain
    print("\nA blockchain é válida?", blockchain.is_chain_valid())

    # Exibe os blocos na blockchain
    for block in blockchain.chain:
        print(
            f"Bloco #{block.index} - Hash: {block.hash} - Dados: {block.data}")


if __name__ == "__main__":
    main()
