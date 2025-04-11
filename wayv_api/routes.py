from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models import db, Participante, participante_schema, participantes_schema
from utils import processa_arquivo, calcular_idade, enviar_dados_wayv, criar_participante_de_dict
from datetime import datetime
import json
import os

api = Blueprint('api', __name__)

@api.route('/participantes', methods=['POST'])
def adicionar_participantes():
    """
    Endpoint para adicionar participantes a partir de um arquivo Excel ou CSV.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Arquivo Excel (.xls, .xlsx) ou CSV (.csv) com os dados dos participantes
    responses:
      200:
        description: Participantes adicionados com sucesso
      400:
        description: Erro na validação dos dados
      500:
        description: Erro interno do servidor
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
    arquivo = request.files['file']
    
    if arquivo.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
    if not arquivo.filename.lower().endswith(('.xls', '.xlsx', '.csv')):
        return jsonify({'error': 'Formato de arquivo inválido. Envie um arquivo Excel (.xls, .xlsx) ou CSV (.csv)'}), 400
    
    print(f"Processando arquivo: {arquivo.filename}")
    participantes_dados = processa_arquivo(arquivo)
    
    if isinstance(participantes_dados, tuple) and 'error' in participantes_dados[0]:
        return jsonify(participantes_dados[0]), participantes_dados[1]
    
    participantes_adicionados = []
    participantes_com_erro = []
    
    for participante_dict in participantes_dados:
        try:
            print(f"Processando participante: {participante_dict}")
            
            if isinstance(participante_dict.get('data_nascimento'), str):
                pass
            elif hasattr(participante_dict.get('data_nascimento'), 'strftime'):
                participante_dict['data_nascimento'] = participante_dict['data_nascimento'].strftime('%Y-%m-%d')
            
            participante_data = participante_schema.load(participante_dict)
            
            if Participante.query.filter_by(email=participante_data['email']).first():
                participantes_com_erro.append({
                    'participante': participante_dict,
                    'error': f"E-mail '{participante_dict['email']}' já está cadastrado"
                })
                continue
                
            participante = criar_participante_de_dict(participante_data)
            db.session.add(participante)
            participantes_adicionados.append(participante_schema.dump(participante))
            
        except ValidationError as err:
            print(f"Erro de validação: {err.messages}")
            participantes_com_erro.append({
                'participante': participante_dict,
                'error': err.messages
            })
        except Exception as e:
            import traceback
            print(f"Erro inesperado: {str(e)}")
            print(traceback.format_exc())
            participantes_com_erro.append({
                'participante': participante_dict,
                'error': f"Erro inesperado: {str(e)}"
            })
    
    db.session.commit()
    
    response = {
        'participantes_adicionados': len(participantes_adicionados),
        'participantes_com_erro': len(participantes_com_erro),
        'detalhes': {
            'adicionados': participantes_adicionados,
            'erros': participantes_com_erro
        }
    }
    
    return jsonify(response), 200


@api.route('/participantes', methods=['GET'])
def listar_participantes():
    """
    Endpoint para listar todos os participantes com filtro opcional por sexo.
    ---
    parameters:
      - name: sexo
        in: query
        type: string
        required: false
        description: Filtro por sexo (Masculino, Feminino, Outros)
    responses:
      200:
        description: Lista de participantes
      500:
        description: Erro interno do servidor
    """
    try:
        sexo = request.args.get('sexo')
        
        if sexo:
            participantes = Participante.query.filter_by(sexo=sexo).all()
        else:
            participantes = Participante.query.all()
            
        return jsonify({
            'total': len(participantes),
            'participantes': participantes_schema.dump(participantes)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao listar participantes: {str(e)}'}), 500


@api.route('/participantes/<int:id>', methods=['PUT'])
def atualizar_participante(id):
    """
    Endpoint para atualizar a data de nascimento de um participante.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do participante
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            data_nascimento:
              type: string
              format: date
              description: Nova data de nascimento (YYYY-MM-DD)
    responses:
      200:
        description: Participante atualizado com sucesso
      404:
        description: Participante não encontrado
      400:
        description: Dados inválidos
      500:
        description: Erro interno do servidor
    """
    print(f"Tentando atualizar participante ID: {id}")
    
    participante = Participante.query.get(id)
    
    if not participante:
        print(f"Participante ID: {id} não encontrado")
        return jsonify({'error': 'Participante não encontrado'}), 404
    
    print(f"Participante atual: {participante_schema.dump(participante)}")
    
    try:
        dados = request.get_json()
        print(f"Dados recebidos: {dados}")
    except Exception as e:
        print(f"Erro ao processar JSON: {str(e)}")
        return jsonify({'error': 'Erro ao processar dados JSON. Verifique o formato da requisição.'}), 400
    
    if not dados or 'data_nascimento' not in dados:
        print("Dados inválidos: data_nascimento não fornecida")
        return jsonify({'error': 'É necessário informar a data de nascimento'}), 400
    
    try:
        #converter a string para data
        nova_data = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        print(f"Nova data de nascimento: {nova_data}")
        
        participante.data_nascimento = nova_data
        participante.idade = calcular_idade(nova_data)
        
        print(f"Atualizando participante ID: {id} - Nova idade: {participante.idade}")
        
        db.session.commit()
        
        participante_atualizado = Participante.query.get(id)
        print(f"Participante após atualização: {participante_schema.dump(participante_atualizado)}")
        
        return jsonify({
            'message': 'Participante atualizado com sucesso',
            'participante': participante_schema.dump(participante_atualizado)
        }), 200
        
    except ValueError as e:
        print(f"Erro de formato de data: {str(e)}")
        return jsonify({'error': 'Formato de data inválido. Use o formato YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Erro ao atualizar participante: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Erro ao atualizar participante: {str(e)}'}), 500


@api.route('/webhook', methods=['POST'])
def receber_webhook():
    """
    Webhook para receber dados de formulários submetidos.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            form_id:
              type: string
            nome_completo:
              type: string
            data_nascimento:
              type: string
              format: date
            sexo:
              type: string
            email:
              type: string
              format: email
    responses:
      200:
        description: Dados processados com sucesso
      400:
        description: Dados inválidos
      500:
        description: Erro interno do servidor
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        campos_obrigatorios = ['form_id', 'nome_completo', 'data_nascimento', 'sexo', 'email']
        if not all(campo in dados for campo in campos_obrigatorios):
            return jsonify({'error': 'Campos obrigatórios não fornecidos'}), 400
        
        try:
            data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use o formato YYYY-MM-DD'}), 400
        
        idade = calcular_idade(data_nascimento)
        
        participante = Participante.query.filter_by(email=dados['email']).first()
        
        if participante:
            participante.nome_completo = dados['nome_completo']
            participante.data_nascimento = data_nascimento
            participante.sexo = dados['sexo']
            participante.idade = idade
            if 'celular' in dados:
                participante.celular = dados['celular']
        else:
            participante = Participante(
                nome_completo=dados['nome_completo'],
                data_nascimento=data_nascimento,
                sexo=dados['sexo'],
                email=dados['email'],
                celular=dados.get('celular')
            )
            db.session.add(participante)
        
        db.session.commit()
        
        resultado_envio = enviar_dados_wayv(dados['form_id'], idade)
        
        return jsonify({
            'message': 'Dados processados com sucesso',
            'participante': participante_schema.dump(participante),
            'idade_calculada': idade,
            'resultado_envio': resultado_envio[0]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao processar dados do webhook: {str(e)}'}), 500


@api.route('/participantes', methods=['DELETE'])
def limpar_base():
    """
    Endpoint para remover todos os registros da base de dados.
    ---
    responses:
      200:
        description: Base de dados limpa com sucesso
      500:
        description: Erro interno do servidor
    """
    try:
        num_deleted = Participante.query.delete()
        db.session.commit()
        
        return jsonify({
            'message': 'Base de dados limpa com sucesso',
            'registros_removidos': num_deleted
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao limpar a base de dados: {str(e)}'}), 500
@api.route('/webhook/status', methods=['POST'])
def webhook_status():
    # Verificação de autenticação
    auth_token = request.headers.get('X-Webhook-Token')
    expected_token = os.environ.get('WEBHOOK_SECRET_TOKEN', 'seu_token_secreto_aqui')
    
    if not auth_token or auth_token != expected_token:
        return jsonify({'error': 'Acesso não autorizado'}), 401