import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import re
from selenium.common.exceptions import TimeoutException

# Configuração do WebDriver
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

# Acesse o SEI
driver.get('https://sei.sistemas.ro.gov.br/sip/login.php?sigla_orgao_sistema=RO&sigla_sistema=SEI')

# Faça login
usuario = driver.find_element(By.ID, 'txtUsuario')
senha = driver.find_element(By.ID, 'pwdSenha')
orgao = driver.find_element(By.ID, 'selOrgao')

usuario.send_keys('00840207255')
senha.send_keys('Setembro10')
orgao.send_keys('SEOSP')
senha.send_keys(Keys.RETURN)

# Função para substituir caracteres especiais por _
def substituir_caracteres_especiais(nome):
    return re.sub(r'[^\w\s]', '_', nome)

# Função para verificar se o download foi concluído
def verificar_downloads(diretorio, timeout=60):
    tempo_inicio = time.time()
    while time.time() - tempo_inicio < timeout:
        arquivos = os.listdir(diretorio)
        arquivos_tmp = [arq for arq in arquivos if arq.endswith('.tmp')]
        arquivos_zip = [arq for arq in arquivos if arq.endswith('.zip')]
        if arquivos_zip:
            return arquivos_zip[0]  # Retorna o primeiro arquivo ZIP encontrado
        time.sleep(1)
    return None

# Função para localizar e clicar no botão de gerar ZIP
def encontrar_botao_gerar_zip(driver):
    contêiner = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'divArvoreAcoes'))
    )
    links = contêiner.find_elements(By.TAG_NAME, 'a')
    for link in links:
        if 'procedimento_gerar_zip' in link.get_attribute('href'):
            return link
    return None

# Carregar os números de processo a partir do CSV
csv_path = os.path.join(os.getcwd(), r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\data\database\numeros_processos.csv')
df_processos = pd.read_csv(csv_path)

# Iterar por cada número de processo
for index, row in df_processos.iterrows():
    numero_processo = row['numero_processo']
    try:
        # Pesquisar processo
        pesquisa = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.ID, 'txtPesquisaRapida'))
        )
        pesquisa.clear()
        pesquisa.send_keys(numero_processo, Keys.RETURN)

        # Aguardar página carregar e mudar para o frame correto
        WebDriverWait(driver, 90).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao"))
        )
        botao_gerar_zip = encontrar_botao_gerar_zip(driver)
        if botao_gerar_zip:
            botao_gerar_zip.click()
            btn_gerar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "btnGerar"))
            )
            btn_gerar.click()
            
            nome_arquivo_final = substituir_caracteres_especiais(numero_processo) + '.zip'
            arquivo_zip = verificar_downloads(download_dir)
            if arquivo_zip:
                print(f"Arquivo ZIP baixado: {arquivo_zip}")
                arquivo_tmp = os.path.join(download_dir, arquivo_zip)
                novo_nome_arquivo = os.path.join(download_dir, nome_arquivo_final)
                if os.path.exists(arquivo_tmp):
                    os.rename(arquivo_tmp, novo_nome_arquivo)
                    print(f"Arquivo renomeado para: {novo_nome_arquivo}")
                else:
                    print("O arquivo temporário não foi encontrado.")
                time.sleep(5)
            else:
                print("Tempo de espera do download expirado.")
            
        # Voltar ao frame principal após cada iteração
        driver.switch_to.default_content()    
    except TimeoutException:
        print("Primeira tentativa falhou, tentando novamente...")
        time.sleep(5)
        pesquisa = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, 'txtPesquisaRapida'))
        )

    except Exception as e:
        print(f"Erro geral ao processar o processo {numero_processo}: {str(e)}")
        driver.save_screenshot(f'erro_{numero_processo}.png')

# Fechar o navegador
driver.quit()


