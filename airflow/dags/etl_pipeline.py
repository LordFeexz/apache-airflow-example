from airflow import DAG
from airflow.operators.python import PythonOperator
from constant import DAG_ID
from datetime import datetime, timezone
import json


def extract_data(**kwargs):
    return kwargs.get('params')


def transform_data(data):
    result = []
    if isinstance(data, str):
        data = json.loads(data.replace("'", "\""))

    if "datas" not in data:
        raise Exception("Key 'datas' tidak ditemukan dalam payload!")

    for item in data["datas"]:
        if item["age"] > 18:
            result.append(item)

    return result


def load_data(data):
    try:
        with open('dags/data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error while saving data to JSON: {e}")
        raise


with DAG(
    dag_id=DAG_ID,
    default_args={
        'owner': 'airflow',
        'start_date': datetime.now().astimezone(timezone.utc),
    },
    description='A simple example DAG',
    schedule_interval=None,
) as dag:
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_args=['{{ ti.xcom_pull(task_ids="extract_data") }}'],
    )

    save_task = PythonOperator(
        task_id='save_data',
        python_callable=load_data,
        op_args=['{{ ti.xcom_pull(task_ids="transform_data") }}'],
    )

    extract_task >> transform_task >> save_task
