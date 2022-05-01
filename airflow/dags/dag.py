"""ELT DAG for Drinks"""

##IMPORT PACKAGES
    #The Dag object is used to instantiate a DAG.
    #The Operators are used to operate the tasks:
        #PythonOperator: execute a Python callable. (similar for BashOperator to execute a Bash command)
        #BigQueryOperator: executes SQL queries.

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.models import Variable
from datetime import datetime
from get_drinks import get_drink
import os
import yaml


config_file = open('/home/airflow/dags/cocktails.yaml', 'r')
config = yaml.safe_load(config_file)

args = {
    'owner': 'bookish journey',
    'email': 'joel.itam2021@gmail.com',
    'retries': 3,
    'depends_on_past': True,
}
path = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(path, 'sql')
elt_path = os.path.join(sql_path, 'elt')
ddl_path = os.path.join(elt_path, 'ddl.sql')
ddl = open(ddl_path, mode='r').read()

params = {
    'bucket': config['bucket'],
    'cocktails_key': config['cocktails_key'],
    'path_auth': config['path_auth']
}


## DEFINE DAG
dag = DAG(
    dag_id='drinks_elt_dag_final',
    default_args=args,
    schedule_interval='0 12 * * *',
    start_date=datetime(2022, 4, 22),
    catchup=True,
    max_active_runs=1
)

## DEFINE TASKS
# Our first task is to extract and load drinks data.
extract_load_task = PythonOperator(
   dag=dag,
    task_id = 'extract_load_task',
    provide_context=True,
    python_callable=get_drink,
    op_kwargs={'bucket': params['bucket'], 'key': params['cocktails_key'], 'path_auth':params['path_auth']}
)

transform_task = BashOperator(
    dag=dag,
    params=params,
    task_id = 'transform_task',
    bash_command='echo "This seccions is for transfor the data" '
)

load_task = BigQueryOperator(
    dag=dag,
    params=params,
    task_id = 'load_task',
    use_legacy_sql=False,
    sql=ddl
)

# SET DEPENDENCY
# extract_load_task will run before transform_task and load_task will run after transform_task 
extract_load_task >> transform_task >> load_task