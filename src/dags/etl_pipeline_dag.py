print("Carregando DAG etl_pipeline")
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from antaq_classes import AntaqDownloader, ZipToCsvConverter, SimpleConcat_PreProcessed, SQLServerLoader
import os

DATA_DIR = '/opt/airflow/data'
RAW_DIR = f'{DATA_DIR}/raw'
PROCESSED_DIR = f'{DATA_DIR}/processed'
PRE_PROCESSED_DIR = f'{DATA_DIR}/pre_processed'
FINAL_DIR = f'{DATA_DIR}/final'

SQL_SERVER = os.getenv('SQL_SERVER')
DATABASE = os.getenv('SQL_DATABASE')
USERNAME = os.getenv('SQL_USERNAME')
PASSWORD = os.getenv('SQL_PASSWORD')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def download_data():
    downloader = AntaqDownloader(headless=True)
    try:
        downloader.download_data([2021, 2022, 2023])
        return "Download concluído com sucesso"
    finally:
        downloader.close()

def process_data():
    converter = ZipToCsvConverter(
        zip_dir=RAW_DIR,
        output_dir=PROCESSED_DIR
    )
    converter.process_all_zips()
    return "Processamento concluído com sucesso"

def concatenate_data():
    processor = SimpleConcat_PreProcessed(
        processed_dir=PROCESSED_DIR,
        final_dir=PRE_PROCESSED_DIR
    )
    processor.process_all()
    return "Concatenação concluída com sucesso"

def load_to_sql():
    """Carrega os dados processados para o SQL Server"""
    loader = SQLServerLoader(
        server=SQL_SERVER,
        database=DATABASE,
        username=USERNAME,
        password=PASSWORD
    )
    
    # Carregar todos os arquivos do diretório pre_processed
    results = []
    for file_name in os.listdir(PRE_PROCESSED_DIR):
        if file_name.endswith('.csv'):
            csv_path = os.path.join(PRE_PROCESSED_DIR, file_name)
            # Remove a extensão .csv para usar como nome da tabela
            table_name = os.path.splitext(file_name)[0]
            try:
                result = loader.load_csv_to_sql(
                    csv_path=csv_path,
                    table_name=table_name
                )
                results.append(result)
            except Exception as e:
                results.append(f"Erro ao carregar {file_name}: {str(e)}")
    
    return "\n".join(results)

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL para dados ANTAQ',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    download_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
    )

    process_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )

    concat_task = PythonOperator(
        task_id='concatenate_data',
        python_callable=concatenate_data,
    )

    load_sql_task = PythonOperator(
        task_id='load_to_sql',
        python_callable=load_to_sql,
    )

    download_task >> process_task >> concat_task >> load_sql_task