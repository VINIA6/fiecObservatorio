
# Pipeline ETL ANTAQ com Apache Airflow

Este projeto implementa um pipeline ETL (Extract, Transform, Load) para processar dados da ANTAQ (Agência Nacional de Transportes Aquaviários) utilizando Apache Airflow em containers Docker.

## 🔧 Pré-requisitos

- Docker
- Docker Compose
- Git
- Python 3.7+

## 🚀 Configuração Inicial

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```bash
env
Airflow
AIRFLOW_UID=50000
AIRFLOW_GID=0
AIRFLOW_USER=airflow
AIRFLOW_PASSWORD=airflow
AIRFLOW_DATABASE=airflow
PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
```
### 3. Estrutura de Diretórios

```bash
├── docker/
│ └── constraints-3.7.txt
├── src/
│ └── dags/
│ ├── etl_pipeline_dag.py
│ └── antaq_classes.py
├── data/
│ ├── processed/
│ └── pre_processed/
├── docker-compose.yml
└── README.md
```

### 4. Inicialização do Docker
Inicie todos os serviços
```bash
docker-compose up -d
```

### 5. Acessar o Airflow

1. Acesse a interface web:
   - URL: `http://localhost:8080`
   - Username: `airflow`
   - Password: `airflow123`
