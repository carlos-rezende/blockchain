from flask import Blueprint, jsonify
from src.blockchain import Blockchain

blockchain_bp = Blueprint('blockchain', __name__)
blockchain = Blockchain()


@blockchain_bp.route('/blockchain', methods=['GET'])
def get_blockchain():
    # Modifique aqui para retornar diretamente a lista de blocos
    chain_data = [block.to_dict() for block in blockchain.chain]
    return jsonify(chain_data), 200


# Endpoint para obter o saldo de um endereço


@blockchain_bp.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance}), 200
