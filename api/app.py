from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from .endpoints.sync import sync_bp
from .endpoints.mine import mine_bp
from .endpoints.block import block_bp
from .endpoints.blockchain import blockchain_bp
from .endpoints.transaction import Transaction_bp
from .endpoints.wallet import wallet_bp

app = Flask(__name__)
# Deve ser armazenada de forma segura em produção
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

CORS(app)  # Allows cross-origin requests

# Usuários fictícios para teste, incluindo o admin
users = {
    "user1": "password1",
    "user2": "password2",
    "admin@admin": "admin1234"
}


@app.route("/")
def home():
    return "<p>API Blockchain</p>"


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Validação de credenciais
    if username not in users or users[username] != password:
        return jsonify({"error": "Usuário ou senha incorretos"}), 401

    # Cria o token JWT
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Exemplo de rota protegida


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Register the blueprints with appropriate URL prefixes
# Adiciona proteção JWT a todas as rotas registradas
app.register_blueprint(block_bp)
app.register_blueprint(blockchain_bp)
app.register_blueprint(Transaction_bp)
app.register_blueprint(wallet_bp)
app.register_blueprint(mine_bp)
app.register_blueprint(sync_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
