from flask import Blueprint, jsonify, request
from src.blockchain import Blockchain


sync_bp = Blueprint('sync', __name__)

# Endpoint para sincronizar com outro nó (simplificado)


@sync_bp.route('/sync', methods=['POST'])
def sync():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Nenhum nó fornecido", 400

    Blockchain.sync_chain(nodes)
    return jsonify({'message': 'Blockchain sincronizada com sucesso!'}), 200
