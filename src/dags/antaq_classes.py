import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import re
import shutil
import zipfile
import pandas as pd
from glob import glob
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import os

class SQLServerLoader:
    def __init__(self, server, database, username, password):
        self.connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
        
    def create_engine_connection(self):
        return create_engine(self.connection_string)
    
    def load_csv_to_sql(self, csv_path, table_name, if_exists='replace'):
        try:
            engine = self.create_engine_connection()
            df = pd.read_csv(csv_path, encoding='utf-8')
            
            for col in df.select_dtypes(include=['object']).columns:
                if df[col].str.contains(r'\d{4}-\d{2}-\d{2}').any():
                    df[col] = pd.to_datetime(df[col])
                    
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists=if_exists,
                index=False,
                chunksize=1000
            )
            
            return f"Dados carregados com sucesso para a tabela {table_name}"
            
        except Exception as e:
            raise Exception(f"Erro ao carregar dados para SQL Server: {str(e)}")
        
class ZipToCsvConverter:
    def __init__(self, zip_dir="data/raw", output_dir="data/processed", delimiter=";", encoding="utf-8"):
        self.zip_dir = zip_dir
        self.output_dir = output_dir
        self.delimiter = delimiter
        self.encoding = encoding
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_zip_file(self, zip_path):
        print(f"Processando o arquivo ZIP: {zip_path}")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for file_name in zf.namelist():
                    if file_name.lower().endswith('.txt'):
                        print(f"  Extraindo o arquivo: {file_name}")
                        try:
                            with zf.open(file_name) as file:
                                df = pd.read_csv(file, delimiter=self.delimiter, encoding=self.encoding)
                        except Exception as e:
                            print(f"Erro ao ler o arquivo {file_name} de {zip_path}: {e}")
                            continue
                        
                        base_txt = os.path.splitext(os.path.basename(file_name))[0]
                        output_file = os.path.join(self.output_dir, f"{base_txt}.csv")
                        
                        try:
                            df.to_csv(output_file, index=False)
                            print(f"  CSV salvo em: {output_file}")
                        except Exception as e:
                            print(f"Erro ao salvar CSV para {file_name}: {e}")
        except Exception as e:
            print(f"Erro ao abrir o arquivo ZIP {zip_path}: {e}")
    
    def process_all_zips(self):
        zip_files = glob(os.path.join(self.zip_dir, "*.zip"))
        if not zip_files:
            print("Nenhum arquivo ZIP encontrado.")
            return
        for zip_path in zip_files:
            self.process_zip_file(zip_path)
    
    def group_files_by_base_name(self):
        csv_files = glob(os.path.join(self.output_dir, "*.csv"))
        pattern = re.compile(r"^(.*?)[_-](\d{4})\.csv$")
        
        for csv_file in csv_files:
            filename = os.path.basename(csv_file)
            match = pattern.match(filename)
            if match:
                base_name = match.group(1)
                target_dir = os.path.join(self.output_dir, base_name)
                os.makedirs(target_dir, exist_ok=True)
                target_file = os.path.join(target_dir, filename)
                print(f"Movendo {csv_file} para {target_file}")
                try:
                    shutil.move(csv_file, target_file)
                except Exception as e:
                    print(f"Erro ao mover o arquivo {filename}: {e}")
            else:
                print(f"Arquivo {filename} não corresponde ao padrão esperado.")

class AntaqDownloader:
    def __init__(self, url="https://web3.antaq.gov.br/ea/sense/download.html#pt", 
                 download_dir="data/raw", headless=True):
        self.url = url
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)
        
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        service = Service('/usr/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)
    
    def get_available_years(self):
        select_element = self.wait.until(EC.presence_of_element_located((By.ID, "anotxt")))
        select_year = Select(select_element)
        year_options = [option.text.strip() for option in select_year.options if option.text.strip().isdigit()]
        available_years = sorted([int(y) for y in year_options])
        return select_year, available_years
    
    def download_data(self, years=None):
        self.driver.get(self.url)
        select_year, available_years = self.get_available_years()
        print("Anos disponíveis encontrados no dropdown:", available_years)
        
        if years is not None:
            years = [int(y) for y in years]
            years_to_process = sorted(list(set(available_years).intersection(set(years))))
            if not years_to_process:
                print("Nenhum dos anos informados está disponível.")
                return
        else:
            years_to_process = available_years
        
        print("Anos a serem processados:", years_to_process)
        
        for ano in years_to_process:
            print(f"\n=== Processando o ano {ano} ===")
            select_year.select_by_visible_text(str(ano))
            self.wait.until(lambda d: d.find_element(By.ID, "lista_arquivosea").text.strip() != "")
            
            links = self.wait.until(EC.presence_of_all_elements_located((
                By.XPATH,
                "//*[@id='lista_arquivosea']//a[contains(text(),'Clique aqui')]"
            )))
            
            if not links:
                print(f"Não foram encontrados links para o ano {ano}.")
                continue
            
            todos_link = links[-1]
            href = todos_link.get_attribute("href")
            print(f"Ano {ano} - Link encontrado: {href}")
            
            if href:
                nome_arquivo = f"todos_{ano}.zip"
                caminho_arquivo = os.path.join(self.download_dir, nome_arquivo)
                print(f"Baixando arquivo para: {caminho_arquivo}")
                try:
                    r = requests.get(href, stream=True)
                    r.raise_for_status()
                    with open(caminho_arquivo, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    print(f"Download do ano {ano} concluído!")
                except Exception as download_error:
                    print(f"Erro ao baixar o arquivo do ano {ano}: {download_error}")
    
    def close(self):
        self.driver.quit()

class SimpleConcat_PreProcessed:
    def __init__(self, processed_dir="data/processed", final_dir="data/pre_processed"):
        self.processed_dir = processed_dir
        self.final_dir = final_dir
        self.pattern = re.compile(r"^(\d{4})([A-Za-z0-9_]+)\.csv$")
        os.makedirs(self.final_dir, exist_ok=True)

    def get_file_groups(self):
        all_files = os.listdir(self.processed_dir)
        file_groups = {}
        
        for filename in all_files:
            match = self.pattern.match(filename)
            if match:
                year_str, base_name = match.groups()
                year = int(year_str)
                file_groups.setdefault(base_name, []).append((year, filename))
        
        return file_groups

    def read_and_process_file(self, year, filename):
        file_path = os.path.join(self.processed_dir, filename)
        print(f"Lendo o arquivo: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            df.columns = [col.strip() for col in df.columns]
            df["ano"] = year
            return df
        except Exception as e:
            print(f"Erro ao ler {filename}: {e}")
            return None

    def process_group(self, base_name, files):
        files.sort(key=lambda x: x[0])
        dfs = []
        
        for year, filename in files:
            df = self.read_and_process_file(year, filename)
            if df is not None:
                dfs.append(df)
        
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True, join="outer")
            
            cols = merged_df.columns.tolist()
            if "ano" in cols:
                cols.remove("ano")
                cols.insert(0, "ano")
                merged_df = merged_df[cols]
            
            output_path = os.path.join(self.final_dir, f"{base_name}.csv")
            merged_df.to_csv(output_path, index=False, sep=";")
            print(f"Arquivo unificado de '{base_name}' salvo em: {output_path}")
        else:
            print(f"Nenhum arquivo processado para o grupo '{base_name}'")

    def process_all(self):
        file_groups = self.get_file_groups()
        
        for base_name, files in file_groups.items():
            self.process_group(base_name, files)
