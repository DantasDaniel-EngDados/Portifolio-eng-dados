from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="primeira_dag_a_ser_rodada",
    schedule=None
) as dag:
    trigger_b = TriggerDagRunOperator(
        task_id="trigger_b",
        trigger_dag_id="tabela_temperatura_diaria"
    )
