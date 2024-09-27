import pandas as pd
import streamlit as st
import re
import os
from io import StringIO


st.set_page_config(layout='wide')


# ------------------------------------------ PIPELINE LISTA-SETOR.CSV

df_setores = pd.read_csv(r'C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\App Monitoramento de Processos\data\raw\lista-setor.csv')

# Criar df's separados para tratar a coluna de documentos
coluna_setor_processo = df_setores[['Setor', 'Processo']]
coluna_documento= df_setores[['Documento']]

# Lista de algarismos romanos
romans = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 
          'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 
          'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 
          'XXVII', 'XXVIII', 'XXIX', 'XXX', 'XXXI', 'XXXII', 'XXXIII', 
          'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX', 
          'XL', 'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV', 'XLVI', 'XLVII', 
          'XLVIII', 'XLIX', 'L']
# Excluir a primeira linha
coluna_documento = coluna_documento.drop(index=0).reset_index()

# Excluir linhas onde o 'Documento' é um algarismo romano
coluna_documento = coluna_documento[~coluna_documento['Documento'].isin(romans)].reset_index()



# Unir os DataFrames lado a lado
df_setor = pd.concat([coluna_documento, coluna_setor_processo], axis=1)



# Função para extrair o protocolo
def extrair_protocolo(texto):
    # Usando regex para encontrar um número de 8 a 12 dígitos em qualquer lugar da string
    protocolo = re.search(r'\b\d{8,12}\b', str(texto))  # Procura um número entre 9 e 11 dígitos
    if protocolo:
        return protocolo.group(0)  # Retorna o número encontrado
    return None

# Aplicar a função na coluna 'Documento' para extrair o protocolo
df_setor['Protocolo'] = df_setor['Documento'].apply(extrair_protocolo)

# Excluir linhas onde a coluna 'Protocolo' tem valores vazios
df_setor = df_setor.dropna(subset=['Protocolo'])




# ------------------------------------------ PIPELINE DADOS_EXTRAIDOS.CSV

df_dados = pd.read_csv(r'C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\App Monitoramento de Processos\data\raw\dados_extraidos.csv', dtype={'Protocolo': str})

df_dados['Data'] = pd.to_datetime(df_dados['Data'], format='%d/%m/%Y',)

# Função para extrair o ID
def extrair_id(texto):
    # Expressão regular para capturar o número entre os hifens
    match = re.search(r'-\s*(\d+)\s*-', texto)
    if match:
        return match.group(1)  # Retorna o ID encontrado
    return None  # Retorna None se não encontrar
df_dados['ID'] = df_dados['Título'].apply(extrair_id)


# Extraindo o nome do documento após o delimitador "-"
df_dados['Documento'] = df_dados['Título'].str.split(' - ').str[-1]




# Renomeando a coluna 
df_dados.rename(columns={'Numero Processo': 'Processo'}, inplace=True)

# Excluindo a coluna original 'título'
df_dados.drop(columns=['Protocolo', 'Título', 'Texto 3', 'Texto 4','Texto 5', 'Texto 6', 'Texto 7', 'Texto 8', 'Texto 9'], inplace=True)


df_dados = df_dados.groupby('ID').agg({
    'Processo': 'first',  # Mantém o primeiro valor
    'Nome': lambda x: ', '.join(x),  # Junta os responsáveis
    'Data': 'first',  # Mantém o primeiro valor
    'Documento': 'first'  # Mantém o primeiro valor
}).reset_index()
df_dados.rename(columns={'ID': 'Protocolo'}, inplace=True)


df_merge = pd.merge(df_dados, df_setor[['Protocolo','Setor']], on='Protocolo', how='left')



# Salvar os dados extraídos em um arquivo CSV
df_setor = pd.DataFrame(df_setor)
csv_setor = os.path.join(os.getcwd(), r'C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\App Monitoramento de Processos\data\processed\df_setor.csv')
df_setor.to_csv(csv_setor, index=False)
print(f"Dados salvos no arquivo: {csv_setor}")
print(type(df_setor))



# Salvar os dados extraídos em um arquivo CSV
df_dados = pd.DataFrame(df_dados)
csv_dados = os.path.join(os.getcwd(), r'C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\App Monitoramento de Processos\data\processed\df_dados.csv')
df_dados.to_csv(csv_dados, index=False)
print(f"Dados salvos no arquivo: {csv_dados}")
print(type(df_dados))


# Salvar os dados extraídos em um arquivo CSV
df_merge = pd.DataFrame(df_merge)
csv_df = os.path.join(os.getcwd(), r'C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\App Monitoramento de Processos\data\processed\df_merge.csv')
df_merge.to_csv(csv_df, index=False)
print(f"Dados salvos no arquivo: {csv_df}")
print(type(df_merge))

df_merge.groupby('Processo')['Protocolo'].count()
