from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente, Veiculo
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('rotas', __name__)

# Rota para cadastrar cliente
@bp.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.json
    # Verifica se o cliente já existe pelo CPF ou Email
    if Cliente.query.filter_by(cpf=dados['cpf']).first() or Cliente.query.filter_by(email=dados['email']).first():
        return jsonify({"erro": "Cliente já cadastrado!"}), 400
    
    senha_hash = generate_password_hash(dados['senha'])
    cliente = Cliente(nome=dados['nome'], cpf=dados['cpf'], email=dados['email'], senha=senha_hash)
    db.session.add(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201

# Rota para login de cliente
@bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    cliente = Cliente.query.filter_by(email=dados['email']).first()
    if cliente and check_password_hash(cliente.senha, dados['senha']):
        return jsonify({"mensagem": "Login bem-sucedido!"})
    return jsonify({"erro": "Credenciais inválidas"}), 401

# Rota para cadastrar veículo
@bp.route('/veiculos', methods=['POST'])
def cadastrar_veiculo():
    dados = request.json
    # Verifica se o modelo do veículo já existe
    if Veiculo.query.filter_by(modelo=dados['modelo'], ano=dados['ano']).first():
        return jsonify({"erro": "Veículo já cadastrado!"}), 400
    
    veiculo = Veiculo(modelo=dados['modelo'], ano=dados['ano'], preco=dados['preco'], disponivel=True)
    db.session.add(veiculo)
    db.session.commit()
    return jsonify({"mensagem": "Veículo cadastrado!"}), 201

# Rota para listar veículos
@bp.route('/veiculos', methods=['GET'])
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return jsonify([{"id": v.id, "modelo": v.modelo, "ano": v.ano, "preco": v.preco, "disponivel": v.disponivel} for v in veiculos])
