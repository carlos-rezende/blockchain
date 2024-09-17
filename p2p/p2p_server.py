from flask import Flask, jsonify, request
from blockchain import Blockchain
from flask_socketio import SocketIO, emit
import requests
import asyncio
import websockets
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Instancia a blockchain
blockchain = Blockchain()

# Lista de nós conectados
peers = set()
connected_nodes = set()  # Para WebSockets


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data), 200


@app.route('/add_node', methods=['POST'])
def register_node():
    data = request.get_json()
    node_address = data.get('node_address')

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
            # Verifica se a cadeia externa é válida e maior antes de substituir
            if len(external_chain) > len(blockchain.chain) and blockchain.is_valid_chain(external_chain):
                blockchain.chain = [blockchain.create_block_from_data(
                    block) for block in external_chain]
    return "Blockchain sincronizada", 200


@app.route('/resolve', methods=['GET'])
def resolve_conflicts():
    replaced = blockchain.resolve_conflicts(peers)
    if replaced:
        return jsonify({"message": "Chain replaced with the longest valid chain"}), 200
    return jsonify({"message": "Local chain is the longest"}), 200


@socketio.on('block_added')
def handle_block_added(data):
    # Verifica se o bloco recebido é válido
    block = blockchain.create_block_from_data(data)
    if blockchain.is_valid_block(block):
        blockchain.add_block(block)
        emit('block_added', data, broadcast=True)
        # Broadcast usando WebSockets para nós conectados
        asyncio.run(broadcast_chain(blockchain.chain))
    else:
        emit('block_rejected', {'error': 'Bloco inválido'}, broadcast=True)


# Funções relacionadas ao WebSocket para comunicação P2P
async def broadcast_chain(chain):
    for node in connected_nodes:
        try:
            await node.send(json.dumps([block.to_dict() for block in chain]))
        except websockets.exceptions.ConnectionClosed:
            connected_nodes.remove(node)


async def handle_node(websocket, path):
    # Adiciona o novo nó à lista de conexões
    connected_nodes.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # Aqui você pode implementar a lógica para lidar com mensagens dos nós
            if data.get('action') == 'new_block':
                block_data = data.get('block')
                block = blockchain.create_block_from_data(block_data)
                if blockchain.is_valid_block(block):
                    blockchain.add_block(block)
                    await broadcast_chain(blockchain.chain)
    finally:
        connected_nodes.remove(websocket)


async def start_p2p_server():
    async with websockets.serve(handle_node, "localhost", 6789):
        await asyncio.Future()  # Mantém o servidor em execução

# Executa os servidores Flask e WebSocket
if __name__ == '__main__':
    # Inicia o servidor WebSocket em um thread separado
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_p2p_server)

    # Inicia o servidor Flask
    socketio.run(app, host='0.0.0.0', port=5000)
