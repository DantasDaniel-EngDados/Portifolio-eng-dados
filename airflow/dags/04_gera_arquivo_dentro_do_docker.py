from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2
import pandas as pd
import os

import configPy

# Caminho absoluto para o arquivo SQL na subpasta ../../sql/media_total.sql
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../sql/media_total.sql"))

CSV_OUTPUT_PATH = '/tmp/temperatura_media_diaria.csv'

PG_CONFIG = {
    # A maioria dos dados já são vindas do .env, deixo como fica:
    'dbname':configPy.dbname, # dbname = os.getenv("POSTGRES_DB")
    'user':configPy.user, # os.getenv("POSTGRES_USER")
    'password':configPy.password, # PEGA DO configPy.py , porém está declarado diretamente na variavel password.
    'host':configPy.host, # Declarado no próprio configPy.py. 
    'port':configPy.port  # # Declarado no próprio configPy.py, mesmos valores passados no .env
}

def export_to_csv():
    with open(SQL_FILE_PATH, 'r') as file:
        query = file.read()
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    colnames = [desc for desc in cursor.description]
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=colnames)
    df.to_csv(CSV_OUTPUT_PATH, index=False)
    cursor.close()
    conn.close()

default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='cria_csv_dentro_do_docker',
    description='Exporta dados do Postgres para CSV sem usar PostgresHook',
    default_args=default_args,
    schedule=None,
    tags=['postgres', 'csv', 'sem_hook']
) as dag:
    exportar_csv = PythonOperator(
        task_id='exportar_csv',
        python_callable=export_to_csv
    )

    exportar_csv
