# # import zipfile
# # import os

# # # Diretório onde os arquivos ZIP estão localizados
# # zip_dir = os.path.join(os.getcwd(), 'downloads')
# # # Diretório base para extrair os arquivos
# # extract_base_dir = os.path.join(zip_dir, 'extracted')

# # # Criar o diretório base de extração, se não existir
# # if not os.path.exists(extract_base_dir):
# #     os.makedirs(extract_base_dir)

# # # Função para extrair arquivos ZIP em pastas separadas
# # def extrair_arquivos_zip(diretorio_zip, diretorio_base_extracao):
# #     for arquivo in os.listdir(diretorio_zip):
# #         if arquivo.endswith('.zip'):
# #             caminho_arquivo = os.path.join(diretorio_zip, arquivo)
# #             # Criar um diretório para extrair o arquivo ZIP
# #             nome_pasta = os.path.splitext(arquivo)[0]  # Nome sem extensão
# #             diretorio_extracao = os.path.join(diretorio_base_extracao, nome_pasta)
            
# #             if not os.path.exists(diretorio_extracao):
# #                 os.makedirs(diretorio_extracao)
            
# #             try:
# #                 with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
# #                     zip_ref.extractall(diretorio_extracao)
# #                 print(f"Arquivo {arquivo} extraído com sucesso para {diretorio_extracao}.")
# #             except zipfile.BadZipFile:
# #                 print(f"O arquivo {arquivo} está corrompido ou não é um arquivo ZIP válido.")
# #             except Exception as e:
# #                 print(f"Ocorreu um erro ao extrair o arquivo {arquivo}: {str(e)}")

# # # Chamar a função para extrair arquivos ZIP
# # extrair_arquivos_zip(zip_dir, extract_base_dir)

# import zipfile
# import os
# import shutil
# import time

# # Diretório onde os arquivos ZIP estão localizados
# zip_dir = os.path.join(os.getcwd(), 'downloads')
# # Diretório base para extrair os arquivos
# extract_base_dir = os.path.join(zip_dir, r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\downloads\extracted')
# # Diretório para armazenar todos os documentos
# pasta_documentos_dir = os.path.join(zip_dir, r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\downloads\pasta_documentos')

# # Criar o diretório base de extração, se não existir
# if not os.path.exists(extract_base_dir):
#     os.makedirs(extract_base_dir)

# # Criar a pasta para armazenar todos os documentos, se não existir
# if not os.path.exists(pasta_documentos_dir):
#     os.makedirs(pasta_documentos_dir)

# # Função para extrair arquivos ZIP em pastas separadas
# def extrair_arquivos_zip(diretorio_zip, diretorio_base_extracao):
#     for arquivo in os.listdir(diretorio_zip):
#         if arquivo.endswith('.zip'):
#             caminho_arquivo = os.path.join(diretorio_zip, arquivo)
#             # Criar um diretório para extrair o arquivo ZIP
#             nome_pasta = os.path.splitext(arquivo)[0]  # Nome sem extensão
#             diretorio_extracao = os.path.join(diretorio_base_extracao, nome_pasta)
            
#             if not os.path.exists(diretorio_extracao):
#                 os.makedirs(diretorio_extracao)
            
#             try:
#                 with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
#                     zip_ref.extractall(diretorio_extracao)
#                 print(f"Arquivo {arquivo} extraído com sucesso para {diretorio_extracao}.")
#             except zipfile.BadZipFile:
#                 print(f"O arquivo {arquivo} está corrompido ou não é um arquivo ZIP válido.")
#             except Exception as e:
#                 print(f"Ocorreu um erro ao extrair o arquivo {arquivo}: {str(e)}")

# # Função para mover todos os documentos extraídos para a pasta_documentos
# def mover_documentos_para_pasta(diretorio_extracao, pasta_documentos):
#     for pasta in os.listdir(diretorio_extracao):
#         caminho_pasta = os.path.join(diretorio_extracao, pasta)
#         if os.path.isdir(caminho_pasta):
#             for arquivo in os.listdir(caminho_pasta):
#                 caminho_arquivo = os.path.join(caminho_pasta, arquivo)
#                 if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith('.html'):
#                     # Tentar mover o arquivo, com um loop de espera
#                     while True:
#                         try:
#                             shutil.move(caminho_arquivo, os.path.join(pasta_documentos, arquivo))
#                             print(f"Arquivo {arquivo} movido para {pasta_documentos}.")
#                             break  # Se o movimento for bem-sucedido, saia do loop
#                         except PermissionError:
#                             print(f"Arquivo {arquivo} em uso. Tentando novamente em 1 segundo...")
#                             time.sleep(1)  # Espera 1 segundo antes de tentar novamente

# # Chamar a função para extrair arquivos ZIP
# extrair_arquivos_zip(zip_dir, extract_base_dir)

# # Chamar a função para mover documentos para a pasta_documentos
# mover_documentos_para_pasta(extract_base_dir, pasta_documentos_dir)

# print("Processo de extração e organização concluído.")

# ------------------ VERSÃO SUBSTITUIR
import zipfile
import os
import shutil
import time

# Diretório onde os arquivos ZIP estão localizados
zip_dir = os.path.join(os.getcwd(), 'downloads')
# Diretório base para extrair os arquivos
extract_base_dir = os.path.join(zip_dir, r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\downloads\extracted')
# Diretório para armazenar todos os documentos
pasta_documentos_dir = os.path.join(zip_dir, r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\downloads\pasta_documentos')
# Diretório para armazenar os arquivos ZIP após a extração
zip_storage_dir = os.path.join(zip_dir, r'C:\Users\00840207255\Desktop\App Monitoramento de Processos\downloads\zip')

# Criar o diretório base de extração, se não existir
if not os.path.exists(extract_base_dir):
    os.makedirs(extract_base_dir)

# Criar a pasta para armazenar todos os documentos, se não existir
if not os.path.exists(pasta_documentos_dir):
    os.makedirs(pasta_documentos_dir)

# Criar a pasta para armazenar os arquivos ZIP após a extração, se não existir
if not os.path.exists(zip_storage_dir):
    os.makedirs(zip_storage_dir)

# Função para extrair arquivos ZIP em pastas separadas, substituindo pastas existentes
def extrair_arquivos_zip(diretorio_zip, diretorio_base_extracao):
    for arquivo in os.listdir(diretorio_zip):
        if arquivo.endswith('.zip'):
            caminho_arquivo = os.path.join(diretorio_zip, arquivo)
            # Criar um diretório para extrair o arquivo ZIP
            nome_pasta = os.path.splitext(arquivo)[0]  # Nome sem extensão
            diretorio_extracao = os.path.join(diretorio_base_extracao, nome_pasta)
            
            # Se a pasta já existir, removê-la antes de extrair o novo conteúdo
            if os.path.exists(diretorio_extracao):
                shutil.rmtree(diretorio_extracao)
                print(f"Substituindo pasta existente: {diretorio_extracao}")

            os.makedirs(diretorio_extracao)  # Cria um novo diretório limpo

            try:
                with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                    zip_ref.extractall(diretorio_extracao)
                print(f"Arquivo {arquivo} extraído com sucesso para {diretorio_extracao}.")
                
                # Mover o arquivo ZIP para a pasta zip_storage_dir após a extração
                shutil.move(caminho_arquivo, os.path.join(zip_storage_dir, arquivo))
                print(f"Arquivo ZIP {arquivo} movido para {zip_storage_dir}.")
                
            except zipfile.BadZipFile:
                print(f"O arquivo {arquivo} está corrompido ou não é um arquivo ZIP válido.")
            except Exception as e:
                print(f"Ocorreu um erro ao extrair o arquivo {arquivo}: {str(e)}")

# Função para mover todos os documentos extraídos para a pasta_documentos, substituindo se já existirem
def mover_documentos_para_pasta(diretorio_extracao, pasta_documentos):
    for pasta in os.listdir(diretorio_extracao):
        caminho_pasta = os.path.join(diretorio_extracao, pasta)
        if os.path.isdir(caminho_pasta):
            for arquivo in os.listdir(caminho_pasta):
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                destino_arquivo = os.path.join(pasta_documentos, arquivo)

                if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith('.html'):
                    # Se o arquivo já existir na pasta de destino, removê-lo antes de mover o novo
                    if os.path.exists(destino_arquivo):
                        os.remove(destino_arquivo)
                        print(f"Substituindo arquivo existente: {destino_arquivo}")
                    
                    # Tentar mover o arquivo, com um loop de espera
                    while True:
                        try:
                            shutil.move(caminho_arquivo, destino_arquivo)
                            print(f"Arquivo {arquivo} movido para {pasta_documentos}.")
                            break  # Se o movimento for bem-sucedido, saia do loop
                        except PermissionError:
                            print(f"Arquivo {arquivo} em uso. Tentando novamente em 1 segundo...")
                            time.sleep(1)  # Espera 1 segundo antes de tentar novamente

# Função para excluir as pastas extraídas após o processo
def excluir_pastas_extracao(diretorio_extracao):
    for pasta in os.listdir(diretorio_extracao):
        caminho_pasta = os.path.join(diretorio_extracao, pasta)
        if os.path.isdir(caminho_pasta):
            try:
                shutil.rmtree(caminho_pasta)
                print(f"Pasta {caminho_pasta} excluída.")
            except Exception as e:
                print(f"Erro ao excluir a pasta {caminho_pasta}: {str(e)}")

# Chamar a função para extrair arquivos ZIP
extrair_arquivos_zip(zip_dir, extract_base_dir)

# Chamar a função para mover documentos para a pasta_documentos
mover_documentos_para_pasta(extract_base_dir, pasta_documentos_dir)

# Excluir as pastas de extração após o processo de movimentação
excluir_pastas_extracao(extract_base_dir)

print("Processo de extração, organização e limpeza concluído.")



