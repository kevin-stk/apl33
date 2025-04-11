import pandas as pd
from datetime import datetime
import requests
from models import Participante
from config import Config

def processa_arquivo(arquivo):
    try:
        #tipo de arquivo pela extensão
        nome_arquivo = arquivo.filename.lower()
        
        if nome_arquivo.endswith('.xlsx') or nome_arquivo.endswith('.xls'):
            df = pd.read_excel(arquivo)
        elif nome_arquivo.endswith('.csv'):
            try:
                df = pd.read_csv(arquivo, encoding='utf-8')
            except UnicodeDecodeError:
                arquivo.seek(0) 
                df = pd.read_csv(arquivo, encoding='latin-1')
        else:
            return {'error': 'Formato de arquivo não suportado. Use .xlsx, .xls ou .csv'}, 400
        
        print(f"Colunas detectadas: {df.columns.tolist()}")
        
        colunas_necessarias = ['Nome Completo', 'Data de Nascimento', 'Sexo', 'E-mail']
        colunas_alternativas = ['nome_completo', 'data_nascimento', 'sexo', 'email']
        
        # verifica o conjunto principal de colunas
        if all(coluna in df.columns for coluna in colunas_necessarias):
            pass 
        elif all(coluna in df.columns for coluna in colunas_alternativas):
            colunas_necessarias = colunas_alternativas
        else:
            print(f"Colunas esperadas: {colunas_necessarias} ou {colunas_alternativas}")
            print(f"Colunas encontradas: {df.columns.tolist()}")
            return {'error': 'O arquivo não contém todas as colunas necessárias'}, 400
        
        df.columns = [col.lower().replace(' ', '_').replace('-', '_') for col in df.columns]
        
        mapeamento_colunas = {
            'nome_completo': 'nome_completo',
            'data_de_nascimento': 'data_nascimento',
            'sexo': 'sexo',
            'e_mail': 'email',
            'celular': 'celular'
        }
        
        df = df.rename(columns=mapeamento_colunas)
        
        print("Amostra de dados processados:")
        print(df.head())
        
        # Converte data_nascimento
        df['data_nascimento'] = pd.to_datetime(df['data_nascimento'])
        df['data_nascimento'] = df['data_nascimento'].dt.strftime('%Y-%m-%d')
        
        sexos_validos = ['Masculino', 'Feminino', 'Outros']
        df['sexo'] = df['sexo'].apply(lambda x: x if x in sexos_validos else 'Outros')

        resultados = df.to_dict('records')
        print(f"Total de registros processados: {len(resultados)}")
        print(f"Exemplo do primeiro registro após processamento: {resultados[0] if resultados else 'Nenhum registro'}")
        return resultados
    except Exception as e:
        import traceback
        print(f"Erro ao processar o arquivo: {str(e)}")
        print(traceback.format_exc())
        return {'error': f'Erro ao processar o arquivo: {str(e)}'}, 500


def calcular_idade(data_nascimento):
    hoje = datetime.now()
    nascimento = datetime.combine(data_nascimento, datetime.min.time())
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    return idade


def enviar_dados_wayv(form_id, idade, status=None):
    token = Config.WAYV_TOKEN
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Preparar os campos para envio
    fields = [
        {
            "field_id": "idade",
            "answer": str(idade)
        }
    ]
    
    # Adicionar status se fornecido
    if status:
        fields.append({
            "field_id": "status",
            "answer": status
        })
    
    payload = {
        "form_entry_id": form_id,
        "template_id": Config.WAYV_TEMPLATE_ID,
        "execution_company_id": Config.WAYV_EXECUTION_COMPANY_ID,
        "fields": fields
    }
    
    try:
        url = "https://app.way-v.com/api/integration/checklists"
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            message = f'Idade {idade} enviada para o formulário {form_id}'
            if status:
                message += f' com status {status}'
            return {'message': message}, 200
        else:
            return {'error': f'Erro ao enviar dados para Wayv: {response.status_code}'}, response.status_code
    except Exception as e:
        return {'error': f'Erro na comunicação com a API Wayv: {str(e)}'}, 500


def criar_participante_de_dict(participante_dict):
    data_nascimento = participante_dict['data_nascimento']
    if isinstance(data_nascimento, str):
        data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    
    return Participante(
        nome_completo=participante_dict['nome_completo'],
        data_nascimento=data_nascimento,
        sexo=participante_dict['sexo'],
        email=participante_dict['email'],
        celular=participante_dict.get('celular')
    )