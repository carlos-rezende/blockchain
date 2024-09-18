from flask import Blueprint, Flask, jsonify, request
from src.blockchain import Blockchain
from src.transaction import Transaction

app = Flask(__name__)

blockchain = Blockchain()
Transaction_bp = Blueprint('transaction', __name__)

# Endpoint para criar uma nova transação


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount',
                'signature', 'sender_public_key']

    # Verifica se os dados obrigatórios estão presentes
    if not all(k in values for k in required):
        return 'Dados ausentes', 400

    # Cria a transação
    transaction = Transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        amount=values['amount'],
        signature=values['signature'],
        sender_public_key=values['sender_public_key']
    )

    # Adiciona a transação à lista de transações pendentes
    if blockchain.create_transaction(transaction):
        return jsonify({'message': 'Transação criada com sucesso'}), 201
    else:
        return jsonify({'message': 'Falha ao criar transação'}), 400

# Endpoint para verificar uma transação específica


@app.route('/transactions/verify', methods=['POST'])
def verify_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount',
                'signature', 'sender_public_key']

    # Verifica se os dados obrigatórios estão presentes
    if not all(k in values for k in required):
        return 'Dados ausentes', 400

    # Cria a transação para verificação
    transaction = Transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        amount=values['amount'],
        signature=values['signature'],
        sender_public_key=values['sender_public_key']
    )

    # Verifica a transação
    if transaction.verify_signature():
        return jsonify({'message': 'Transação válida'}), 200
    else:
        return jsonify({'message': 'Transação inválida'}), 400
