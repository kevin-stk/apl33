import os
import sqlite3
from flask import Flask
from models import db

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')

try:
    print(f"Tentando criar banco de dados em: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.close()
    print("Teste de conexão SQLite bem-sucedido!")
except Exception as e:
    print(f"Erro ao conectar diretamente via SQLite: {e}")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")