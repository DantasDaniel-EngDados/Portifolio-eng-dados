import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

import configPy

DATA_PATH = "/opt/airflow/leituras"
FILE_NAME = "leituras_de_temperaturas.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../sql/insert_temperatura_media.sql"))

default_args = {
    "owner": "você",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "tabela_temperatura_media_diaria",
    default_args=default_args,
    description="Insere valor médio de temperatura no banco de dados",
    schedule="@daily",
    start_date=datetime(2025, 8, 20),
    catchup=False
) as dag:

    @task
    def verificar_arquivo():
        file_path = os.path.join(DATA_PATH, FILE_NAME)
        if os.path.isfile(file_path):
            print(f"Arquivo encontrado: {file_path}")
            return file_path
        else:
            raise FileNotFoundError(f"Arquivo {file_path} não encontrado")

    @task
    def extrair_transformar(file_path):
        print(f"Lendo arquivo: {file_path}")
        df = pd.read_csv(file_path)
        df["data"] = pd.to_datetime(df["data"]).dt.date
        df_agg = df.groupby(["cidade", "data"], as_index=False)["temperatura"].mean()
        df_agg = df_agg.rename(columns={"temperatura": "temperatura_media"})
        return df_agg.to_dict(orient="records")

    @task
    def carregar(dados):
        with open(SQL_FILE_PATH, "r") as f:
            insert_query = f.read()
        conn = psycopg2.connect(
            # A maioria dos dados já são vindas do .env, deixo como fica:
            dbname=configPy.dbname, # dbname = os.getenv("POSTGRES_DB")
            user=configPy.user, # os.getenv("POSTGRES_USER")
            password=configPy.password, # PEGA DO configPy.py , porém está declarado diretamente na variavel password.
            host=configPy.host, # Declarado no próprio configPy.py. 
            port=configPy.port  # # Declarado no próprio configPy.py, mesmos valores passados no .env 
        )
        cursor = conn.cursor()
        for row in dados:
            cursor.execute(insert_query, (row["cidade"], row["data"], row["temperatura_media"]))
        conn.commit()
        cursor.close()
        conn.close()

    arquivo = verificar_arquivo()
    dados_agrupados = extrair_transformar(arquivo)
    carregar(dados_agrupados)

    trigger_a = TriggerDagRunOperator(
        task_id="trigger_a",
        trigger_dag_id="cria_csv_dentro_do_docker"
    )

    carregar(dados_agrupados) >> trigger_a

