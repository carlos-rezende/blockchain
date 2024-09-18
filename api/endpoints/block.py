from flask import Blueprint, jsonify, request
from src.blockchain import Blockchain

blockchain = Blockchain()
block_bp = Blueprint('block', __name__)


@block_bp.route('/blocks', methods=['GET'])
def get_blocks():
    """
    Retrieve the entire blockchain.
    """
    chain_data = [block.to_dict() for block in blockchain.chain]
    return jsonify(chain_data), 200


@block_bp.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    """
    Retrieve a specific block by its index.
    """
    if index < len(blockchain.chain):
        block = blockchain.chain[index]
        return jsonify(block.to_dict()), 200
    else:
        return jsonify({"error": "Block not found"}), 404


@block_bp.route('/mine', methods=['POST'])
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
