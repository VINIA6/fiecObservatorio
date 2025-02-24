FROM apache/airflow:2.5.1

# Instalar Chrome e ChromeDriver
USER root
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    xvfb \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0

# Configurar variáveis de ambiente para o Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/src"
ENV DISPLAY=:99

# Criar diretório para downloads
RUN mkdir -p /opt/airflow/data/raw && \
    chown -R airflow: /opt/airflow/data

# Copiar requirements e código fonte
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt
COPY --chown=airflow:root src /opt/airflow/src/

# Criar diretórios e ajustar permissões
RUN mkdir -p /opt/airflow/src/etl && \
    touch /opt/airflow/src/etl/__init__.py && \
    chown -R airflow: /opt/airflow/src

# Mudar para usuário airflow para instalar dependências
USER airflow

# Instalar dependências Python
RUN pip install --user --no-cache-dir -r /opt/airflow/requirements.txt

# Verificar a instalação
RUN echo "Verificando instalação do selenium..." && \
    python -c "import selenium; print(f'Selenium instalado em: {selenium.__file__}')"

# Instalar dependências do SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*
