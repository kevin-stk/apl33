import pandas as pd

dados = [
    {'Nome Completo': 'João Carlos', 'Data de Nascimento': '1995-08-15', 'Sexo': 'Masculino', 'E-mail': 'joao.silva@gmail.com', 'Celular': '(11) 98765-4321'},
    {'Nome Completo': 'Maria Lúcia', 'Data de Nascimento': '1997-04-22', 'Sexo': 'Feminino', 'E-mail': 'maria.oliveira@yahoo.com.br', 'Celular': '(21) 97654-3210'},
    {'Nome Completo': 'Carlos Antonio', 'Data de Nascimento': '1998-11-30', 'Sexo': 'Masculino', 'E-mail': 'carlos.p@gmail.com', 'Celular': '(31) 96543-2109'},
    {'Nome Completo': 'Ana Mara', 'Data de Nascimento': '1996-01-05', 'Sexo': 'Feminino', 'E-mail': 'ana.costa@outlook.com', 'Celular': '(41) 95432-1098'},
    {'Nome Completo': 'Thiago Júnior', 'Data de Nascimento': '1993-09-19', 'Sexo': 'Masculino', 'E-mail': 'thiago.martins@empresa.com.br', 'Celular': '(51) 94321-0987'},
    {'Nome Completo': 'Sofia Loren', 'Data de Nascimento': '1994-05-25', 'Sexo': 'Feminino', 'E-mail': 'sofia.g@hotmail.com', 'Celular': '(61) 93210-9876'},
    {'Nome Completo': 'Bruno Lauro', 'Data de Nascimento': '1992-03-10', 'Sexo': 'Masculino', 'E-mail': 'bruno.souza@live.com', 'Celular': '(71) 92109-8765'},
    {'Nome Completo': 'Clara Maria', 'Data de Nascimento': '1999-12-14', 'Sexo': 'Feminino', 'E-mail': 'clara.mendes@gmail.com', 'Celular': '(81) 91098-7654'},
    {'Nome Completo': 'Felipe Lucas', 'Data de Nascimento': '1990-07-29', 'Sexo': 'Masculino', 'E-mail': 'felipe.nasc@uol.com.br', 'Celular': '(91) 90987-6543'},
    {'Nome Completo': 'Laura Martha', 'Data de Nascimento': '1995-02-23', 'Sexo': 'Feminino', 'E-mail': 'laura.rocha@bol.com.br', 'Celular': '(11) 90876-5432'}
]

df = pd.DataFrame(dados)

colunas_corretas = {
    'Nome Completo': 'nome_completo',
    'Data de Nascimento': 'data_nascimento',
    'Sexo': 'sexo',
    'E-mail': 'email',
    'Celular': 'celular'
}

df = df.rename(columns=colunas_corretas)

df.to_csv('participantes_correto.csv', index=False, encoding='utf-8')

print("Arquivo CSV gerado com sucesso: participantes_correto.csv")

print("\nPrimeiras linhas do arquivo:")
print(df.head())