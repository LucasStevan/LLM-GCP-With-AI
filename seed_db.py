import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import requests
import io
import numpy as np

# Autenticação
# Substitua pelo caminho do seu arquivo de chave JSON do GCP e certifique-se de que ele tenha as permissões necessárias para acessar o BigQuery.
path_to_json = 'projectkey_from_your_gcp.json'  
credentials = service_account.Credentials.from_service_account_file(path_to_json)

PROJECT_ID = 'your-gcp-project-id' 
DATASET_ID = 'your_bigquery_dataset'
TABLE_NAME = 'your_bigquery_table'

# URL do CSV com os dados completos dos municípios
URL_DATASET = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/csv/municipios.csv"

print("Iniciando extração de dados públicos...")

try:
    # Download do csv
    response = requests.get(URL_DATASET)
    response.raise_for_status()
    
    df = pd.read_csv(io.StringIO(response.text))

    # Colunas originais no CSV: codigo_ibge, nome, latitude, longitude, capital, codigo_uf, siafi_id, ddd, fuso_horario
    df_final = df[[
        'codigo_ibge', 'nome', 'latitude', 'longitude', 
        'capital', 'codigo_uf', 'siafi_id', 'ddd', 'fuso_horario'
    ]].copy()

    # Simulação extra

    print("Simulando dados financeiros para 2000 municípios...")
    
    df_final = df_final.head(2000)
    
    df_final['valor_empenhado'] = np.random.uniform(500000.0, 50000000.0, size=len(df_final)).round(2)
    df_final['ano'] = 2023
    df_final['funcao_governo'] = np.random.choice(
        ['Saúde', 'Educação', 'Segurança', 'Cultura', 'Saneamento'], 
        size=len(df_final)
    )

    print(f"Dataset preparado com {df_final.shape[1]} colunas e {len(df_final)} linhas.")

    # Envio para o BigQuery
    full_table_path = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"
    
    print(f"Enviando dados para {full_table_path}...")
    
    df_final.to_gbq(
        destination_table=full_table_path,
        project_id=PROJECT_ID,
        credentials=credentials,
        if_exists='replace'
    )

    print("Sucesso! A tabela foi populada com dados geográficos e financeiros.")

except Exception as e:
    print(f"Erro no processo: {e}")