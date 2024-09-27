# from bs4 import BeautifulSoup
# import re
# import pandas as pd
# import os
# import glob

# # Função para extrair o número do processo
# def extrair_numero_processo(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     # Procurar pelo elemento <td> com a informação de referência do processo
#     td_element = soup.find('td', align='left', style="font-family:Calibri;font-size:9pt;border:0;", width="80%")
    
#     # Extrair o número do processo usando expressão regular
#     numero_processo = None
#     if td_element:
#         texto = td_element.get_text()
#         numero_processo = re.search(r'\d{4}\.\d{6}\/\d{4}-\d{2}', texto)
#         if numero_processo:
#             return numero_processo.group(0)
#     return None

# # Função para extrair nomes, cargos, protocolos e chaves QR do conteúdo HTML
# def extrair_dados(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     # Encontrar todos os elementos <p> com o estilo específico
#     p_elements = soup.find_all('p', style="margin:0;text-align: justify; font-size:11pt;font-family: Calibri;")
    
#     nomes = []
#     datas = []
#     protocolos = []
    
#     nome_atual = ""
#     data_atual = ""
#     protocolo_atual = ""

    
#     for p_element in p_elements:
#         texto = p_element.get_text()

#         # Extrair o nome (tag <b>)
#         b_elements = p_element.find_all('b')
#         for b in b_elements:
#             nome_atual = b.get_text(strip=True)
#             nomes.append(nome_atual)

#             # Limpar os valores de cargos, protocolo e chave QR para nova entrada
#             cargo_atual = ""
#             protocolo_atual = ""

#         # Extrair a data (padrão dd/mm/yyyy)
#         data = re.search(r'\d{2}/\d{2}/\d{4}', texto)
#         if data:
#             data_atual = data.group(0)

#         # Extrair o cargo, protocolo e chave QR
#         protocolo = re.search(r'\d{10}', texto)

#         protocolo_atual = protocolo.group(0) if protocolo else protocolo_atual

#         # Adiciona a entrada completa, apenas se o nome estiver preenchido
#         if nome_atual:
#             nomes.append(nome_atual)
#             datas.append(data_atual)
#             protocolos.append(protocolo_atual)

#     return nomes, datas, protocolos

# # Função para processar os arquivos HTML
# def processar_arquivos_html(diretorio):
#     arquivos_html = glob.glob(os.path.join(diretorio, "*.html"))  # Filtrar apenas arquivos HTML
#     data = []

#     for arquivo in arquivos_html:
#         with open(arquivo, 'r', encoding='latin') as file:
#             html_content = file.read()

#             # Extrair dados do arquivo
#             nomes, datas, protocolos = extrair_dados(html_content)
#             numero_processo = extrair_numero_processo(html_content)

#             # Criar uma lista de dicionários com os dados agrupados
#             for nome, data_processo, cargo, protocolo, chave_qr in zip(nomes, datas, protocolos):
#                 if nome:  # Adicionar apenas linhas com nomes válidos
#                     data.append({
#                         'Numero Processo': numero_processo,
#                         'Nome': nome,
#                         'Data': data_processo,
#                         'Protocolo do Documento': protocolo,
#                     })

#     # Criar DataFrame e salvar em CSV
#     df = pd.DataFrame(data)
#     df.to_csv('C:\Users\00840207255\OneDrive\SESAU\01 GAD\App Monitoramento de Processos\data\raw\dados_extraidos.csv', index=False)
#     print("Dados extraídos e salvos em r'C:\Users\00840207255\OneDrive\SESAU\01 GAD\App Monitoramento de Processos\data\raw\dados_extraidos.csv'")

# # Definir o caminho da pasta com os arquivos HTML
# diretorio = r"C:\Users\00840207255\OneDrive\SESAU\01 GAD\App Monitoramento de Processos\downloads\pasta_documentos"
# processar_arquivos_html(diretorio)


# # Diretório onde estão os arquivos HTML
# html_directory = r'C:\Users\00840207255\OneDrive\SESAU\01 GAD\App Monitoramento de Processos\downloads\pasta_documentos'

# # Lista para armazenar os dados
# data = []

# # Função para extrair dados usando seletores CSS
# def extract_data(file_path):
#     with open(file_path, 'r', encoding='latin') as file:
#         soup = BeautifulSoup(file, 'lxml')
        
#         # Extração do título
#         title_tag = soup.find('title')
#         title = title_tag.get_text(strip=True) if title_tag else 'N/A'
        
#         # Extração usando seletores CSS
#         text_3 = soup.select_one('body > p:nth-child(3)')
#         text_4 = soup.select_one('body > p:nth-child(4)')
#         text_5 = soup.select_one('body > p:nth-child(5)')
#         text_6 = soup.select_one('body > p:nth-child(6)')
#         text_7 = soup.select_one('body > p:nth-child(7)')
#         text_8 = soup.select_one('body > p:nth-child(8)')
#         text_9 = soup.select_one('body > p:nth-child(9)')



#         text_3_content = text_3.get_text(strip=True) if text_3 else 'N/A'
#         text_4_content = text_4.get_text(strip=True) if text_4 else 'N/A'
#         text_5_content = text_5.get_text(strip=True) if text_5 else 'N/A'
#         text_6_content = text_6.get_text(strip=True) if text_6 else 'N/A'
#         text_7_content = text_7.get_text(strip=True) if text_7 else 'N/A'
#         text_8_content = text_8.get_text(strip=True) if text_8 else 'N/A'
#         text_9_content = text_9.get_text(strip=True) if text_9 else 'N/A'



#         return {
#             'Título': title,
#             'Texto 3': text_3_content,
#             'Texto 4': text_4_content,
#             'Texto 5': text_5_content,
#             'Texto 6': text_6_content,
#             'Texto 7': text_7_content,
#             'Texto 8': text_8_content,
#             'Texto 9': text_9_content,

#         }
    
# # Processa todos os arquivos HTML no diretório
# for filename in os.listdir(html_directory):
#     if filename.endswith('.html'):
#         file_path = os.path.join(html_directory, filename)
#         extracted_data = extract_data(file_path)
#         data.append(extracted_data)

# # Cria um DataFrame com pandas
# df = pd.DataFrame(data)

# # Salva o DataFrame em um arquivo CSV
# csv_file_path = r'C:\Users\00840207255\OneDrive\SESAU\01 GAD\App Monitoramento de Processos\data\raw\dados_extraidos.csv'
# df.to_csv(csv_file_path, index=False)

# print(f'Dados salvos em {csv_file_path}')

from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import glob

# Função para extrair o número do processo
def extrair_numero_processo(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Procurar pelo elemento <td> com a informação de referência do processo
    td_element = soup.find('td', align='left', style="font-family:Calibri;font-size:9pt;border:0;", width="80%")
    numero_processo = None
    if td_element:
        texto = td_element.get_text()
        numero_processo = re.search(r'\d{4}\.\d{6}\/\d{4}-\d{2}', texto)
        if numero_processo:
            return numero_processo.group(0)
    return None

# Função para extrair datas, nomes, e protocolos do conteúdo HTML
def extrair_dados(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    p_elements = soup.find_all('p', style="margin:0;text-align: justify; font-size:11pt;font-family: Calibri;")
    
    nomes = []
    datas = []
    protocolos = []
    
    nome_atual = ""
    data_atual = ""
    protocolo_atual = ""

    for p_element in p_elements:
        texto = p_element.get_text()
        b_elements = p_element.find_all('b')
        for b in b_elements:
            nome_atual = b.get_text(strip=True)
            nomes.append(nome_atual)

        data = re.search(r'\d{2}/\d{2}/\d{4}', texto)
        if data:
            data_atual = data.group(0)

        protocolo = re.search(r'\d{10}', texto)
        protocolo_atual = protocolo.group(0) if protocolo else protocolo_atual

        if nome_atual:
            nomes.append(nome_atual)
            datas.append(data_atual)
            protocolos.append(protocolo_atual)

    return nomes, datas, protocolos

# Função para extrair conteúdo textual com seletores CSS
def extrair_texto(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else 'N/A'
    
    # Selecionando elementos de parágrafos específicos
    text_3 = soup.select_one('body > p:nth-child(3)')
    text_4 = soup.select_one('body > p:nth-child(4)')
    text_5 = soup.select_one('body > p:nth-child(5)')
    text_6 = soup.select_one('body > p:nth-child(6)')
    text_7 = soup.select_one('body > p:nth-child(7)')
    text_8 = soup.select_one('body > p:nth-child(8)')
    text_9 = soup.select_one('body > p:nth-child(9)')

    return {
        'Título': title,
        'Texto 3': text_3.get_text(strip=True) if text_3 else 'N/A',
        'Texto 4': text_4.get_text(strip=True) if text_4 else 'N/A',
        'Texto 5': text_5.get_text(strip=True) if text_5 else 'N/A',
        'Texto 6': text_6.get_text(strip=True) if text_6 else 'N/A',
        'Texto 7': text_7.get_text(strip=True) if text_7 else 'N/A',
        'Texto 8': text_8.get_text(strip=True) if text_8 else 'N/A',
        'Texto 9': text_9.get_text(strip=True) if text_9 else 'N/A',
    }

# Função para processar os arquivos HTML
def processar_arquivos_html(diretorio):
    arquivos_html = glob.glob(os.path.join(diretorio, "*.html"))  # Filtrar apenas arquivos HTML
    data = []

    for arquivo in arquivos_html:
        with open(arquivo, 'r', encoding='latin') as file:
            html_content = file.read()

            # Extrair dados
            numero_processo = extrair_numero_processo(html_content)
            nomes, datas, protocolos = extrair_dados(html_content)
            conteudo_texto = extrair_texto(html_content)

            # Criar uma lista de dicionários com os dados agrupados
            for nome, data_processo, protocolo in zip(nomes, datas, protocolos):
                if nome:  # Adicionar apenas linhas com nomes válidos
                    data.append({
                        'Numero Processo': numero_processo,
                        'Nome': nome,
                        'Data': data_processo,
                        'Protocolo': protocolo,
                        **conteudo_texto,  # Mescla o conteúdo textual com os outros dados
                    })

    # Criar DataFrame e salvar em CSV
    df = pd.DataFrame(data)
    csv_path = r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\data\raw\dados_extraidos.csv'
    df.to_csv(csv_path, index=False)
    print(f'Dados extraídos e salvos em {csv_path}')

# Definir o caminho da pasta com os arquivos HTML
diretorio = r"C:\Users\00840207255\Desktop\App Monitoramento de Processos\downloads\pasta_documentos"
processar_arquivos_html(diretorio)
