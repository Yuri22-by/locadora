from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.routes import bp as rotas_bp  # Importando o blueprint de rotas

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'  # Caminho para o banco de dados
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    # Registrando o blueprint
    app.register_blueprint(rotas_bp, url_prefix='/api')  # Isso garante que as rotas começam com /api

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Criar as tabelas no banco de dados
    app.run(debug=True)
