from airflow import DAG
from database import get_connection
from airflow.operators.python import PythonOperator
from constant import DAG_ID
from datetime import datetime


def extract_data(**kwargs):
    print(kwargs, "kwargs")
    data = kwargs['dag_run'].conf
    if not data:
        raise Exception("No data received!")

    return data


def transform_data(data):
    # assume this process to transform data
    result = []
    for item in data:
        print(item, "item")
        if item['age'] > 18:
            result.append(item)

    return result


def load_data(data):
    print(data, "data")
    conn = get_connection()
    cursor = conn.cursor()

    for item in data:
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)",
                       (item['name'],
                        item['age']))

    conn.commit()
    conn.close()


with DAG(
    dag_id=DAG_ID,
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2023, 1, 1), },
    description='A simple example DAG',
    schedule_interval=None,
    start_date=datetime.now(),
) as dag:
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,
        op_kwargs={
            'data': '{{ task_instance.xcom_pull(task_ids="extract_data") }}'},
    )

    save_task = PythonOperator(
        task_id='save_to_db',
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            'data': '{{ task_instance.xcom_pull(task_ids="transform_data") }}'},
    )

    extract_task >> transform_task >> save_task
