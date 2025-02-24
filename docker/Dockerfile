FROM apache/airflow:2.7.1

USER root

# Instalar dependências do sistema e SQL Server
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
    libgtk-3-0 \
    gnupg2 \
    curl \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 unixodbc-dev \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    && ln -s /opt/mssql-tools18/bin/sqlcmd /usr/bin/sqlcmd \
    && ln -s /opt/mssql-tools18/bin/bcp /usr/bin/bcp \
    && rm -rf /var/lib/apt/lists/*

# Configurar variáveis de ambiente
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    PYTHONPATH="${PYTHONPATH}:/opt/airflow/src" \
    DISPLAY=:99 \
    PATH="$PATH:/opt/mssql-tools18/bin"

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

USER airflow

# Instalar dependências Python
RUN pip install --user --no-cache-dir -r /opt/airflow/requirements.txt \
    && pip install --user --no-cache-dir pyodbc==4.0.39

# Verificar instalações
RUN echo "Verificando instalação do selenium..." && \
    python -c "import selenium; print(f'Selenium instalado em: {selenium.__file__}')" && \
    echo "Verificando instalação do pyodbc..." && \
    python -c "import pyodbc; print(f'pyodbc instalado em: {pyodbc.__file__}')" && \
    echo "Verificando instalação do sqlcmd..." && \
    which sqlcmd
