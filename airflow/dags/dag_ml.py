"""ML DAG for Drinks"""

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
import os
import yaml
from kmeans_training import kmeans_training



config_file = open('/home/airflow/dags/GCP_model_details.yaml', 'r')
config = yaml.safe_load(config_file)

args = {
    'owner': 'bookish journey',
    'email': 'noreply@bookishjourney.com',
    'retries': 1,
    'depends_on_past': True,
}

path = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(path, 'sql')
ml_path = os.path.join(sql_path, 'ml')
bigquery_csv_path = os.path.join(ml_path, 'bigquery_csv.sql')
bqcsv = open(bigquery_csv_path, mode='r').read()

params = {
    'bucket': config['bucket_name'],
    'path_auth': config['path_auth']
}

## DEFINE DAG
dag = DAG(
    dag_id='drinks_ml_dag',
    default_args=args,
    schedule_interval='0 12 * * *',
    start_date=datetime(2022, 4, 22),
    catchup=True,
    max_active_runs=1
)


## DEFINE TASKS
bqcsv_task = BigQueryOperator(
	     dag=dag,
    	     task_id = 'bqcsv_task',
    	     use_legacy_sql=False,
     	     sql=bqcsv
 )

ml_setup_task = BashOperator(
    dag=dag,
    params=params,
    task_id = 'ml_setup_task',
    bash_command='./GCP_model_setup.sh'
)

ml_load_csv = BashOperator(
    dag=dag,
    params=params,
    task_id = 'ml_load_csv',
    bash_command='sudo gsutil cp gs://cocktails-bucket/testing/000000000000.csv /home/airflow/dags/'
)

kmeans_training_task = PythonOperator(
    dag=dag,
    task_id = 'kmeans_training_task',
    provide_context=True,
    python_callable=kmeans_training
)

kmeans_test_task = BashOperator(
    dag=dag,
    params=params,
    task_id = 'kmeans_test_task',
    bash_command='python3 /home/airflow/dags/kmeans_test.py'
)

meanshift_training_task = BashOperator(
    dag=dag,
    params=params,
    task_id = 'meanshift_training_task',
    bash_command='python3 /home/airflow/dags/meanshift_training.py'
)
meanshift_test_task = BashOperator(
    dag=dag,
    params=params,
    task_id = 'meanshift_test_task',
    bash_command='python3 /home/airflow/dags/meanshift_test.py'
)

# SET DEPENDENCY
bqcsv_task >> ml_setup_task >> ml_load_csv >> kmeans_training_task >> kmeans_test_task

bqcsv_task >> ml_setup_task >> ml_load_csv >> meanshift_training_task >> meanshift_test_task


