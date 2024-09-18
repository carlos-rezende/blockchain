from flask import Blueprint, jsonify, request
from src.blockchain import Blockchain

blockchain = Blockchain()
mine_bp = Blueprint('mine', __name__)


# Endpoint para minerar os blocos
@mine_bp.route('/mine', methods=['GET'])
def mine():
    # Minera as transações pendentes
    blockchain.mine_pending_transactions('Minerador1')
    return jsonify({'message': 'Bloco minerado com sucesso!'}), 200


@mine_bp.route('/mine_block', methods=['POST'])
def mine_block():
    """
    Mine a new block and add it to the blockchain.
    Requires a JSON body with 'miner_address'.
    """
    data = request.json
    miner_address = data.get('miner_address')

    if not miner_address:
        return jsonify({"error": "miner_address is required"}), 400

    # Mine the block and reward the miner
    blockchain.mine_pending_transactions(miner_address)
    return jsonify({"message": "New block mined!", "block": blockchain.chain[-1].to_dict()}), 201


