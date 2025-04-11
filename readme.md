Esta é uma API desenvolvida como parte do teste técnico para integração com a plataforma Wayv. A API permite gerenciar e integrar dados de formulários, com funcionalidades para inserção, listagem, atualização e remoção de registros.


wayv_api/
├── app.py             # Arquivo principal da aplicação
├── config.py          # Configurações da aplicação
├── models.py          # Modelos de dados/banco
├── routes.py          # Endpoints da API
├── utils.py           # Funções utilitárias
├── .env               # Variáveis de ambiente (opcional)
├── requirements.txt   # Dependências do projeto
└── dados_participantes.py  # Script para gerar arquivo de exemplo

- **Inserção de Dados**: Endpoint para inserir dados de um arquivo Excel
- **Listagem de Dados**: Endpoint para listar todos os registros com filtros por sexo
- **Atualização de Dados**: Endpoint para atualizar a data de nascimento dos participantes
- **Webhook de Recebimento**: Endpoint para receber dados automaticamente quando um formulário é submetido
- **Limpeza de Dados**: Endpoint para remover todos os registros da base de dados


- **Linguagem de Programação**: Python 3.9+
- **Framework**: Flask
- **Banco de Dados**: SQLite
- **Bibliotecas Principais**: SQLAlchemy, Pandas, Marshmallow, Flasgger
- **Documentação**: Swagger UI


# pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes do Python)


1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/wayv-api-teste.git
   cd wayv-api-teste
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente (opcional):
   - Renomeie o arquivo `.env.example` para `.env`
   - As configurações padrão já estão definidas no código, mas podem ser personalizadas no arquivo .env

# Executando a API

Para iniciar a API localmente:

```bash
python app.py
```

A API estará disponível em:
- Local: http://localhost:5000
- Documentação Swagger: http://localhost:5000/swagger/

# Endpoints da API

# 1. Inserir Participantes via Excel

- **URL**: `/api/participantes`
- **Método**: `POST`
- **Parâmetros**:
  - `file` (Multipart Form): Arquivo Excel (.xls ou .xlsx)
- **Resposta de Sucesso**:
  ```json
  {
    "participantes_adicionados": 5,
    "participantes_com_erro": 0,
    "detalhes": {
      "adicionados": [...],

# Exemplos de Requisições para a API Wayv

Este documento contém exemplos de como usar cada endpoint da API. Você pode utilizar ferramentas como Postman, cURL ou o próprio Swagger UI para testar as requisições.

# 1. Inserir Participantes (Upload de Excel)

**Endpoint:** `POST /api/participantes`

**cURL:**
```bash
curl -X POST \
  http://localhost:5000/api/participantes \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/caminho/para/participantes.xlsx'
```

**Postman:**
1. Método: POST
2. URL: http://localhost:5000/api/participantes
3. Body: form-data
4. Key: file (tipo file)
5. Value: selecione o arquivo Excel

**Resposta de exemplo:**
```json
{
  "participantes_adicionados": 10,
  "participantes_com_erro": 0,
  "detalhes": {
    "adicionados": [
      {
        "id": 1,
        "nome_completo": "João Carlos",
        "data_nascimento": "1995-08-15",
        "sexo": "Masculino",
        "email": "joao.silva@gmail.com",
        "celular": "(11) 98765-4321",
        "idade": 29,
        "data_criacao": "2025-04-09T10:15:30.123456",
        "data_atualizacao": "2025-04-09T10:15:30.123456"
      },
      // ... outros participantes
    ],
    "erros": []
  }
}
```

# 2. Listar Participantes

# 2.1 Listar Todos os Participantes

**Endpoint:** `GET /api/participantes`

**cURL:**
```bash
curl -X GET http://localhost:5000/api/participantes
```

**Postman:**
1. Método: GET
2. URL: http://localhost:5000/api/participantes

**Resposta de exemplo:**
```json
{
  "total": 10,
  "participantes": [
    {
      "id": 1,
      "nome_completo": "João Carlos",
      "data_nascimento": "1995-08-15",
      "sexo": "Masculino",
      "email": "joao.silva@gmail.com",
      "celular": "(11) 98765-4321",
      "idade": 29,
      "data_criacao": "2025-04-09T10:15:30.123456",
      "data_atualizacao": "2025-04-09T10:15:30.123456"
    },
    // ... outros participantes
  ]
}
```

# 2.2 Filtrar por Sexo

**Endpoint:** `GET /api/participantes?sexo=Masculino`

**cURL:**
```bash
curl -X GET "http://localhost:5000/api/participantes?sexo=Masculino"
```

**Postman:**
1. Método: GET
2. URL: http://localhost:5000/api/participantes?sexo=Masculino

**Resposta de exemplo:**
```json
{
  "total": 5,
  "participantes": [
    {
      "id": 1,
      "nome_completo": "João Carlos",
      "data_nascimento": "1995-08-15",
      "sexo": "Masculino",
      "email": "joao.silva@gmail.com",
      "celular": "(11) 98765-4321",
      "idade": 29,
      "data_criacao": "2025-04-09T10:15:30.123456",
      "data_atualizacao": "2025-04-09T10:15:30.123456"
    },
    // ... outros participantes masculinos
  ]
}
```

# 3. Atualizar Data de Nascimento

**Endpoint:** `PUT /api/participantes/{id}`

**cURL:**
```bash
curl -X PUT \
  http://localhost:5000/api/participantes/1 \
  -H 'Content-Type: application/json' \
  -d '{
    "data_nascimento": "1994-09-15"
  }'
```

**Postman:**
1. Método: PUT
2. URL: http://localhost:5000/api/participantes/1
3. Body: raw, JSON
4. Conteúdo:
```json
{
  "data_nascimento": "1994-09-15"
}
```

**Resposta de exemplo:**
```json
{
  "message": "Participante atualizado com sucesso",
  "participante": {
    "id": 1,
    "nome_completo": "João Carlos",
    "data_nascimento": "1994-09-15",
    "sexo": "Masculino",
    "email": "joao.silva@gmail.com",
    "celular": "(11) 98765-4321",
    "idade": 30,
    "data_criacao": "2025-04-09T10:15:30.123456",
    "data_atualizacao": "2025-04-09T11:20:45.789012"
  }
}
```

# 4. Webhook para Receber Dados

**Endpoint:** `POST /api/webhook`

**cURL:**
```bash
curl -X POST \
  http://localhost:5000/api/webhook \
  -H 'Content-Type: application/json' \
  -d '{
    "form_id": "form_12345",
    "nome_completo": "Roberto Silva",
    "data_nascimento": "1988-07-12",
    "sexo": "Masculino",
    "email": "roberto.silva@exemplo.com",
    "celular": "(11) 91234-5678"
  }'
```

**Postman:**
1. Método: POST
2. URL: http://localhost:5000/api/webhook
3. Body: raw, JSON
4. Conteúdo:
```json
{
  "form_id": "form_12345",
  "nome_completo": "Roberto Silva",
  "data_nascimento": "1988-07-12",
  "sexo": "Masculino",
  "email": "roberto.silva@exemplo.com",
  "celular": "(11) 91234-5678"
}
```

**Resposta de exemplo:**
```json
{
  "message": "Dados processados com sucesso",
  "participante": {
    "id": 11,
    "nome_completo": "Roberto Silva",
    "data_nascimento": "1988-07-12",
    "sexo": "Masculino",
    "email": "roberto.silva@exemplo.com",
    "celular": "(11) 91234-5678",
    "idade": 36,
    "data_criacao": "2025-04-09T12:30:15.654321",
    "data_atualizacao": "2025-04-09T12:30:15.654321"
  },
  "idade_calculada": 36,
  "resultado_envio": {
    "message": "Idade 36 enviada para o formulário form_12345"
  }
}
```

# 5. Limpar Base de Dados

**Endpoint:** `DELETE /api/participantes`

**cURL:**
```bash
curl -X DELETE http://localhost:5000/api/participantes
```

**Postman:**
1. Método: DELETE
2. URL: http://localhost:5000/api/participantes

**Resposta de exemplo:**
```json
{
  "message": "Base de dados limpa com sucesso",
  "registros_removidos": 11
}


