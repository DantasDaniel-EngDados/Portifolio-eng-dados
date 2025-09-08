FROM apache/airflow:3.0.2

USER root

# Cria diretório e instala redis-tools
RUN mkdir -p /opt/airflow/leituras && \
    mkdir -p /opt/sql && \
    mkdir -p /tmp && \
    mkdir -p /opt/airflow/leituraDevolvida && \
    apt-get update && \
    apt-get install -y redis-tools && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia arquivo CSV para dentro do container
COPY ./leituras/leituras_de_temperaturas.csv /opt/airflow/leituras
COPY ./sql/insert_temperatura_media.sql /opt/sql
COPY ./sql/insert_temperatura_dados.sql /opt/sql
COPY ./sql/media_total.sql /opt/sql


USER airflow
