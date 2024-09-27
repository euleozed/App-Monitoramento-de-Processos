import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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

# Carregar os números de processo a partir do CSV
csv_path = os.path.join(os.getcwd(), r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\data\database\numeros_processos.csv')
print(f"Carregando números de processo do arquivo CSV: {csv_path}")
df_processos = pd.read_csv(csv_path)

# Lista para armazenar todos os dados de processos
todos_dados_processos = []

# Iterar por cada número de processo
print("Iniciando a iteração pelos números de processo...")
for index, row in df_processos.iterrows():
    numero_processo = row['numero_processo']
    print(f"Processando o número de processo: {numero_processo}")
    
    try:
        # Pesquisar processo
        print(f"Pesquisando processo {numero_processo}...")
        pesquisa = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.ID, 'txtPesquisaRapida'))
        )
        pesquisa.clear()
        pesquisa.send_keys(numero_processo, Keys.RETURN)
        print(f"Processo {numero_processo} pesquisado com sucesso.")

        # Alternar para o primeiro iframe onde está o botão de "Consultar Andamento"
        print("Alternando para o iframe 'ifrArvore'...")
        WebDriverWait(driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, 'ifrArvore'))
        )
        print("Iframe 'ifrArvore' selecionado com sucesso.")

        # Expandir árvore usando imagem
        print("Expandindo a árvore de documentos...")
        expandir_xpath = "//img[@src='/infra_css/svg/mais.svg']"
        expandir = WebDriverWait(driver, 90).until(
            EC.element_to_be_clickable((By.XPATH, expandir_xpath))
        )
        expandir.click()  # Clicar para expandir a árvore
        time.sleep(5)  # Pausar para garantir que os documentos carreguem totalmente
        print("Árvore expandida com sucesso.")
        
        # Obter o HTML do iframe e passar para o BeautifulSoup
        print("Obtendo o HTML do iframe e processando com BeautifulSoup...")
        html_arvore = driver.page_source
        soup = BeautifulSoup(html_arvore, 'html.parser')

        # Localizar os elementos dos documentos e setores diretamente com Selenium
        documentos = driver.find_elements(By.CLASS_NAME, "infraArvoreNo")
        setores = driver.find_elements(By.CLASS_NAME, "infraArvoreInformacao")

        # Verificar se documentos e setores foram encontrados
        if documentos and setores:
            print(f"Encontrados {len(documentos)} documentos e {len(setores)} setores para o processo {numero_processo}.")
        else:
            print(f"Nenhum documento ou setor encontrado para o processo {numero_processo}.")

        # Iterar pelos documentos e setores encontrados
        for documento, setor in zip(documentos, setores):
            nome_documento = documento.text.strip()
            nome_setor = setor.text.strip()
            todos_dados_processos.append({
                "Documento": nome_documento,
                "Setor": nome_setor,
                "Processo": numero_processo
            })
            print(f"Documento: {nome_documento}, Setor: {nome_setor} adicionado.")

    except Exception as e:
        print(f"Erro ao processar o número de processo {numero_processo}: {e}")
    
    # Sair do iframe para continuar a navegação
    print(f"Saindo do iframe após processar o processo {numero_processo}.")
    driver.switch_to.default_content()

# Salvar os dados extraídos em um arquivo CSV
print("Salvando os dados extraídos em um arquivo CSV...")
df_resultado = pd.DataFrame(todos_dados_processos)
csv_output_path = os.path.join(os.getcwd(), r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\data\raw\lista-setor.csv')
df_resultado.to_csv(csv_output_path, index=False)
print(f"Dados salvos no arquivo: {csv_output_path}")

# Encerrar o navegador
print("Encerrando o navegador.")
driver.quit()
