from flask import Flask, jsonify, request
from blockchain import Blockchain
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Instancia a blockchain
blockchain = Blockchain()

# Lista de nós conectados
peers = set()


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data), 200


@app.route('/add_node', methods=['POST'])
def register_node():
    node_address = request.get_json()['node_address']
    if not node_address:
        return "Endereço do nó inválido", 400

    # Adiciona o nó à lista
    peers.add(node_address)
    return "Nó adicionado com sucesso", 201


@app.route('/sync_chain', methods=['GET'])
def sync_chain():
    for node in peers:
        response = requests.get(f'{node}/chain')
        if response.status_code == 200:
            external_chain = response.json()
            if len(external_chain) > len(blockchain.chain):
                blockchain.chain = [blockchain.create_block_from_data(
                    block) for block in external_chain]
    return "Blockchain sincronizada", 200


@socketio.on('block_added')
def handle_block_added(data):
    block = blockchain.create_block_from_data(data)
    blockchain.add_block(block)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
