from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

class Participante(db.Model):
    __tablename__ = 'participantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    celular = db.Column(db.String(20), nullable=True)
    idade = db.Column(db.Integer, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, nome_completo, data_nascimento, sexo, email, celular=None):
        self.nome_completo = nome_completo
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.email = email
        self.celular = celular
        hoje = datetime.now()
        born = datetime.combine(data_nascimento, datetime.min.time())
        self.idade = hoje.year - born.year - ((hoje.month, hoje.day) < (born.month, born.day))
    
    def __repr__(self):
        return f'<Participante {self.nome_completo}>'


class ParticipanteSchema(Schema):
    id = fields.Int(dump_only=True)
    nome_completo = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    data_nascimento = fields.Date(required=True, format='%Y-%m-%d')  # Formato específico para data
    sexo = fields.Str(required=True, validate=validate.OneOf(['Masculino', 'Feminino', 'Outros']))
    email = fields.Email(required=True)
    celular = fields.Str(validate=validate.Length(max=20))
    idade = fields.Int(dump_only=True)
    data_criacao = fields.DateTime(dump_only=True)
    data_atualizacao = fields.DateTime(dump_only=True)


participante_schema = ParticipanteSchema()
participantes_schema = ParticipanteSchema(many=True)