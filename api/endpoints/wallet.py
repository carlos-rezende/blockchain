from flask import Blueprint, jsonify, request
from src.wallet import Wallet
from src.transaction import Transaction

wallet_bp = Blueprint('wallet', __name__)
wallets = {}  # Dicionário para armazenar as wallets criadas


@wallet_bp.route('/wallet/new', methods=['POST'])
def create_wallet():
    """
    Cria uma nova carteira (wallet) e retorna a chave pública.
    """
    new_wallet = Wallet()
    # Gera um ID para a carteira com base na quantidade de carteiras criadas
    wallet_id = len(wallets)
    wallets[wallet_id] = new_wallet
    public_key = new_wallet.get_public_key()
    return jsonify({"wallet_id": wallet_id, "public_key": public_key.decode('utf-8')}), 201


@wallet_bp.route('/wallet/<int:wallet_id>/public_key', methods=['GET'])
def get_public_key(wallet_id):
    """
    Retorna a chave pública da carteira especificada.
    """
    wallet = wallets.get(wallet_id)
    if not wallet:
        return jsonify({"error": "Carteira não encontrada"}), 404

    public_key = wallet.get_public_key()
    return jsonify({"public_key": public_key.decode('utf-8')}), 200


@wallet_bp.route('/wallet/<int:wallet_id>/sign', methods=['POST'])
def sign_transaction(wallet_id):
    """
    Assina uma transação com a carteira especificada.
    """
    wallet = wallets.get(wallet_id)
    if not wallet:
        return jsonify({"error": "Carteira não encontrada"}), 404

    data = request.json
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')

    if not sender or not recipient or not amount:
        return jsonify({"error": "Dados da transação ausentes"}), 400

    transaction = Transaction(
        sender=sender, recipient=recipient, amount=amount)
    signature = wallet.sign_transaction(transaction)
    return jsonify({"signature": signature.hex()}), 200
