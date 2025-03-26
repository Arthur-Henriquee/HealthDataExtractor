import os
import requests
from bs4 import BeautifulSoup
import zipfile

# Passo 1: Acessar o site
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code != 200:
    print("Falha ao acessar o site!")
    exit()

# Passo 2: Analisar o conteúdo HTML da página
soup = BeautifulSoup(response.text, 'html.parser')

# Passo 3: Encontrar os links para os anexos PDF (Anexo I e II)
pdf_links = []

# Encontrar todos os links para PDFs
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.pdf'):
        pdf_links.append(href)

# Verificar se encontrou os PDFs necessários
if len(pdf_links) < 2:
    print("Não foi possível encontrar os arquivos PDF!")
    exit()

# Passo 4: Fazer o download dos arquivos PDF
pdf_filenames = []

for i, pdf_url in enumerate(pdf_links[:2]):  # Apenas os dois primeiros PDFs
    # Construir o caminho completo para o arquivo
    filename = f'anexo_{i+1}.pdf'
    pdf_filenames.append(filename)
    
    # Fazer o download
    pdf_data = requests.get(pdf_url)
    
    with open(filename, 'wb') as f:
        f.write(pdf_data.content)
    print(f"Arquivo {filename} baixado com sucesso!")

# Passo 5: Compactar os arquivos PDF em um arquivo ZIP
zip_filename = 'anexos.zip'

with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for pdf_filename in pdf_filenames:
        zipf.write(pdf_filename)
        print(f"{pdf_filename} adicionado ao arquivo {zip_filename}")

print(f"Todos os arquivos foram compactados com sucesso em {zip_filename}")
