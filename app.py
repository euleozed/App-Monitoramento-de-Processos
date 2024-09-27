import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

st.set_page_config(
    layout="wide",
    page_title="Início",
    
)

# Título
st.markdown(
    "<h1 style='text-align: center;'>LINHA DO TEMPO DE PROCESSOS ⏳</h1>",
    unsafe_allow_html=True
)
# Personalizar a sidebar
st.text("Resumo de andamentos de processos da gerência de compras - SESAU/RO")
st.divider()
# st.sidebar.header('Menu de Filtros')

df = pd.read_csv(r'data/processed/df_merge.csv', dtype={'Protocolo': str})

# Convertendo a coluna 'Data' para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
df.info()

df.groupby('Processo')['Protocolo'].count()


# Ordenando o DataFrame pelo número do processo e pela data
df = df.sort_values(by=['Processo', 'Data']).reset_index(drop=True)

# Criando a coluna para a quantidade de dias entre o documento 2 e o documento 1
df['Dias entre Documentos'] = df.groupby('Processo')['Data'].diff().dt.days

# Criando a coluna para a quantidade de dias acumulados entre o primeiro documento e o documento atual
df['Dias Acumulados'] = df.groupby('Processo')['Data'].transform(lambda x: (x - x.min()).dt.days)



# Criando o selectbox para escolher o processo
processo_selecionado = st.selectbox('Digite o n° do processo SEi:', options=df['Processo'].value_counts().index, index=None, placeholder="")

# Filtrando o DataFrame com base no processo selecionado
df_selected = df[df['Processo'] == processo_selecionado]


# Definindo o novo registro
data_hoje = datetime.now()  # Variável com a data de hoje
novo_registro = {
    'Processo': processo_selecionado,  # O processo selecionado
    'Data': data_hoje,                  # A data de hoje
    'Protocolo': "",        # Protocolo padrão
    'Nome': "sem andamento",
    'Documento': "sem andamento",        # Documento padrão
    'Setor': '',                         # Preencher conforme necessário
    'Dias entre Documentos': 0,         # Inicializando como 0 ou outro valor
    'Dias Acumulados': 0                 # Inicializando como 0 ou outro valor
}
# Adicionando o novo registro ao DataFrame
df_selected = pd.concat([df_selected, pd.DataFrame([novo_registro])], ignore_index=True)

# Recalculando as colunas 'Dias entre Documentos' e 'Dias Acumulados'
df_selected['Dias entre Documentos'] = df_selected.groupby('Processo')['Data'].diff().dt.days
df_selected['Dias Acumulados'] = df_selected.groupby('Processo')['Data'].transform(lambda x: (x - x.min()).dt.days)


# Figura
df_selected['Dias entre Documentos'] = df_selected['Dias entre Documentos'].fillna(0)
df_selected['Texto'] = df_selected['Documento'] + ' (' + df_selected['Protocolo'] + ') - ' + df_selected['Dias entre Documentos'].astype(int).astype(str) + ' dias'
df_selected['Data Documento'] = df_selected['Data'].dt.strftime('%d/%m/%y')

df_view = df_selected[['Protocolo', 'Documento', 'Nome', 'Dias entre Documentos', 'Data Documento']].sort_values(by='Dias entre Documentos', ascending=False).head(10)
df_table = df_selected[['Texto', 'Nome','Setor', 'Dias Acumulados', 'Dias entre Documentos','Data Documento']].sort_values(by='Dias Acumulados', ascending=True)
# [['Texto', 'Nome','Setor', 'Dias Acumulados', 'Data']]

df_fig = df_selected.nlargest(10, 'Dias entre Documentos').sort_values(by='Data')
fig = px.line(df_fig, 
              x='Data Documento',  # Usando a data formatada para o eixo x
              y='Dias entre Documentos', 
              title=f'Linha do Tempo do Processo: {processo_selecionado}', 
              markers=True, 
              text='Texto')  # Exibindo o protocolo nos markers
fig.update_traces(textposition="top center")
fig
on = st.toggle("Mostrar linha do tempo completa em tabela")
if on:
    st.dataframe(df_table, hide_index=True, width=1750)


df_setor_prazos_geral = df_selected.groupby('Setor').agg(Dias=("Dias entre Documentos", "sum")).sort_values(by="Dias").reset_index()
fig_prazos = px.bar(df_setor_prazos_geral,
                    x='Setor',
                    y='Dias', 
                    title=f'Duração acumulada em cada setor',
                    text_auto=True)
fig_prazos.update_traces(textposition="outside")
fig_prazos
