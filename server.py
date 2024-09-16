from flask import Flask, jsonify, request
from blockchain import Blockchain
from transaction import Transaction

app = Flask(__name__)

# Cria uma instância da blockchain
blockchain = Blockchain()

# Endpoint para obter a cadeia completa


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data), 200

# Endpoint para adicionar uma transação


@app.route('/transaction', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    if not tx_data.get('sender') or not tx_data.get('recipient') or not tx_data.get('amount'):
        return 'Transação inválida', 400

    transaction = Transaction(
        tx_data['sender'], tx_data['recipient'], tx_data['amount'])
    blockchain.create_transaction(transaction)
    return 'Transação adicionada', 201

# Endpoint para minerar transações


@app.route('/mine', methods=['GET'])
def mine_transactions():
    miner_address = request.args.get('miner')
    blockchain.mine_pending_transactions(miner_address)
    return 'Bloco minerado!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
