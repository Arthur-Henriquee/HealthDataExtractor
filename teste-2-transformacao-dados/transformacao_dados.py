import pandas as pd
import zipfile
import os
import pdfplumber

def extrair_tabelas_pdf(arquivo_pdf):
    dados_extraidos = []
    
    if not os.path.exists(arquivo_pdf):
        print(f"Erro: O arquivo {arquivo_pdf} não foi encontrado.")
        return None
    
    with pdfplumber.open(arquivo_pdf) as pdf:
        num_paginas = len(pdf.pages)
        print(f"O PDF contém {num_paginas} páginas.")
        
        for i, pagina in enumerate(pdf.pages, start=1):
            print(f"Extraindo dados da página {i}...")
            tabela = pagina.extract_table()
            
            if tabela:
                dados_extraidos.extend(tabela)
            else:
                print(f"Aviso: Não foi possível extrair uma tabela da página {i}")
    
    return dados_extraidos

def salvar_csv(dados, nome_arquivo):
    if not dados:
        print("Erro: Nenhum dado para salvar.")
        return
    
    df = pd.DataFrame(dados)
    df = df.applymap(lambda x: x.replace('\n', ' ') if isinstance(x, str) else x)  # Remove quebras de linha
    df.to_csv(nome_arquivo, index=False, header=False)
    print(f"Dados salvos no arquivo CSV: {nome_arquivo}")

def criar_arquivo_zip(arquivos, nome_zip):
    with zipfile.ZipFile(nome_zip, 'w') as zipf:
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                zipf.write(arquivo, os.path.basename(arquivo))
            else:
                print(f"Aviso: O arquivo {arquivo} não foi encontrado e não será incluído no ZIP.")
    print(f"Arquivo ZIP criado: {nome_zip}")

def main():
    arquivo_pdf = "C:\\Users\\Arthur\\Downloads\\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

    nome_csv = "rol_procedimentos.csv"
    nome_zip = "Teste_Arthur.zip"
    
    dados = extrair_tabelas_pdf(arquivo_pdf)
    if dados:
        salvar_csv(dados, nome_csv)
        criar_arquivo_zip([nome_csv], nome_zip)
        print("Processamento concluído! O arquivo ZIP foi criado.")
    else:
        print("Erro: Nenhum dado foi extraído do PDF.")

if __name__ == "__main__":
    main()
