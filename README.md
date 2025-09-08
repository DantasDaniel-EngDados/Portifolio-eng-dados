Projeto de portifólio, onde o Airflow recebe um arquivo CSV, e o usuário rodar a Dag primeira_dag_a_ser_rodada para rodar as demais DAGs, que alimenta os bancos de dados com media de temperatura e outro com as temperaturas diarias. Caso queira, deixei o comando para exportar a tabela de media diaria abaixo.
OBS: projeto criado na própria máquina, sistema Windows, usando Docker Desktop.

Os comandos são rodados no CMD a partir da pasta airflow:

    Para iniciar, rodar :
    docker-compose build --no-cache
    docker-compose up airflow-init
    docker-compose up


    Para conferir se criou as tabelas:
    docker exec -it airflow-postgres-1 psql -U nome_usuario -d nome_do_banco_de_dado
    \dt

    Para salvar dentro da pasta leituraDevolvida:
    docker cp airflow-airflow-worker-1:/tmp/temperatura_media_diaria.csv ..\leituraDevolvida\temperatura_media_diaria.csv

No arquivo .env(Fica dentro da pasta airflow):

    AIRFLOW_UID= (por padrão é 50000)
    POSTGRES_USER=
    POSTGRES_DB=
    POSTGRES_PASSWORD=
    AIRFLOW_WWW_USER_PASSWORD=
    AIRFLOW_WWW_USER_USERNAME=
    POSTGRES_PORTS= (por padrão é 5432)
    AIRFLOW_ADMIN_USERNAME=
    AIRFLOW_ADMIN_PASSWORD=
    AIRFLOW_ADMIN_EMAIL=
    AIRFLOW_ADMIN_FIRSTNAME=
    AIRFLOW_ADMIN_LASTNAME= (pode ser valor vazio "")
    AIRFLOW__WEBSERVER__SECRET_KEY= ( gere usa chave secreta)
    AIRFLOW__CORE__FERNET_KEY= {
        #em python:
        from cryptography.fernet import Fernet
        fernet_key = Fernet.generate_key()
        print(fernet_key.decode())
    }

no arquivo configPy.py(Fica dentro da pasta dags, dentro da pasta airflow):

    import os
    from dotenv import load_dotenv

    dotenv_path = '/opt/airflow/.env'
    load_dotenv(dotenv_path)

    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = "" (password deve ser declarado diretamanete aqui)
    host = "postgres"
    port = 

O arquivo airflow/config/airflow.cfg também não foi enviado por conter informações sensíveis.