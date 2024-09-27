import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time
import os

# Configuração do WebDriver
print("Configurando o WebDriver...")
service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
download_dir = os.path.join(os.getcwd(), 'downloads')
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

# Acessando o SEI
print("Acessando o site do SEI...")
driver.get('https://sei.sistemas.ro.gov.br/sip/login.php?sigla_orgao_sistema=RO&sigla_sistema=SEI')

# Realizando login
print("Fazendo login no SEI...")
usuario = driver.find_element(By.ID, 'txtUsuario')
senha = driver.find_element(By.ID, 'pwdSenha')
orgao = driver.find_element(By.ID, 'selOrgao')

usuario.send_keys('00840207255')
senha.send_keys('Setembro10')
orgao.send_keys('SEOSP')
senha.send_keys(Keys.RETURN)
print("Login efetuado com sucesso.")

# Diretório onde os arquivos HTML serão salvos
html_save_dir = r"C:\Users\00840207255\Desktop\App Monitoramento de Processos\downloads\html_documents"
if not os.path.exists(html_save_dir):
    os.makedirs(html_save_dir)

# Carregar os números de processo a partir do CSV
csv_path = os.path.join(os.getcwd(), r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\data\database\numeros_processos.csv')
print(f"Carregando números de processo do arquivo CSV: {csv_path}")
df_processos = pd.read_csv(csv_path)

# Lista para armazenar todos os dados dos processos
todos_dados_processos = []

# Função para baixar o HTML de cada documento
def baixar_html_documento(numero_protocolo, documento_url, documento_nome):
    try:
        # Navegar até o documento clicando no link
        driver.get(documento_url)
        
        # Esperar até que o iframe de visualização do documento esteja disponível
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao"))
        )

        # Esperar até que o conteúdo do iframe esteja disponível
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Capturar o conteúdo HTML da página
        page_html = driver.page_source
        html_file_path = os.path.join(html_save_dir, f'{numero_protocolo}_{documento_nome}.html')
        
        # Salvar o conteúdo HTML no arquivo
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(page_html)
        
        print(f"HTML do documento '{documento_nome}' do processo {numero_protocolo} salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao baixar HTML do documento {documento_nome} do processo {numero_protocolo}: {str(e)}")

# Função para processar cada processo e baixar os documentos HTML
def processar_processo(numero_protocolo):
    try:
        # Pesquisar processo
        pesquisa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'txtPesquisaRapida'))
        )
        pesquisa.clear()
        pesquisa.send_keys(numero_protocolo, Keys.RETURN)
        print(f"Processo {numero_protocolo} pesquisado.")

        # Alternar para o iframe onde está a árvore de documentos
        WebDriverWait(driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, 'ifrArvore'))
        )
        print(f"Iframe 'ifrArvore' selecionado para o processo {numero_protocolo}.")

        # Expandir a árvore de documentos, se necessário
        try:
            expandir = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@src='/infra_css/svg/mais.svg']"))
            )
            expandir.click()
            time.sleep(3)  # Aguardar o carregamento da árvore expandida
            print(f"Árvore de documentos expandida para o processo {numero_protocolo}.")
        except Exception as e:
            print(f"Erro ao expandir a árvore de documentos do processo {numero_protocolo}: {str(e)}")

        # Obter o HTML da árvore de documentos
        html_arvore = driver.page_source
        soup = BeautifulSoup(html_arvore, 'html.parser')

        # Buscar todos os links de documentos (elementos <a> com href que contém 'id_documento')
        documentos = soup.find_all('a', href=True)

        for documento in documentos:
            href = documento['href']
            if 'id_documento' in href:
                # Obter o nome do documento
                nome_documento = documento.text.strip()
                documento_url = f"https://sei.sistemas.ro.gov.br/{href}"

                # Verificar se o documento é HTML e baixar o conteúdo
                if 'html' in nome_documento.lower():  # Verificação se o documento é do tipo HTML
                    print(f"Baixando HTML do documento '{nome_documento}' do processo {numero_protocolo}...")
                    baixar_html_documento(numero_protocolo, documento_url, nome_documento)

    except Exception as e:
        print(f"Erro ao processar o processo {numero_protocolo}: {str(e)}")

    finally:
        # Sempre voltar para o conteúdo principal e recarregar a página inicial de busca
        driver.switch_to.default_content()
        driver.get('https://sei.sistemas.ro.gov.br/')

# Iterar por cada número de processo e processar os documentos
for index, row in df_processos.iterrows():
    numero_protocolo = str(row['numero_processo'])
    processar_processo(numero_protocolo)
    
# Fechar o navegador ao final
driver.quit()