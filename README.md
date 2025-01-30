# apache-airflow-example

step

- cd dags
- install poetry if you dont have it
- add export AIRFLOW_CORE_DAGS_FOLDER="YOUR DIRECTORY" && if your directory is not on airflow dags directory
- run :

  - poetry run airflow db init
  - export AIRFLOW**CORE**DAGS_FOLDER="YOUR DIRECTORY" && poetry run airflow webserver --port 8080
  - export AIRFLOW**CORE**DAGS_FOLDER="YOUR DIRECTORY" && poetry run airflow scheduler
  - poetry run python app.py

- cd functions
- run npm run start:azure
