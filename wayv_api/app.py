import os
from flask import Flask, jsonify, redirect, request
from flasgger import Swagger
from models import db
from routes import api
from config import Config
import ngrok
from dotenv import load_dotenv

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'database.db')
    
    if test_config is None:
        app.config.from_object(Config)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    else:
        app.config.from_mapping(test_config)
    
    app.config['SWAGGER'] = {
        'title': 'API Wayv - Teste de Integração',
        'description': 'API para integração com a plataforma Wayv.',
        'version': '1.0.0',
        'uiversion': 3,
        'specs_route': '/swagger/'
    }
    swagger = Swagger(app)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route('/')
    def index():
        return redirect('/swagger/')
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Endpoint não encontrado'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'error': 'Método não permitido'}), 405
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return app


load_dotenv()

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    
    # Configure o authtoken
    ngrok.set_auth_token('2vZ6NXsZ2WMTsjSolSjmklFzTkA_6aVSev2DCqNEMEhwRqDHx')  # Substitua pelo seu token real
    
    # Inicia o túnel ngrok
    public_url = ngrok.connect(port).public_url
    print(f" * API Wayv rodando em http://localhost:{port}")
    print(f" * Documentação disponível em http://localhost:{port}/swagger/")
    print(f" * Webhook URL pública: {public_url}/api/webhook")
    print(f" * Webhook Status URL: {public_url}/api/webhook/status")
    
    app.run(debug=True, port=port)