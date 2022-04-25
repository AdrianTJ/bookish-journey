
# Readme

This folder contains the following files:

- **dag.py** : This is the file that creates the DAG orchestration.
- **sql_elt_ddl.sql** : This file creates the SQL table where we grab the jsons we previously defined and transform them into a single table.
- **get_drinks.py**: This file contains the functions that we call to grab the data from the cocktails API and create the initial json files.

## Where to find these files?

The files created by the Dags can be found in specified bucket in yaml file called by *cocktails.yaml*.

The tables created in bigquery by *sql_elt_ddl* can be found in bigquery space (*indredients_dag* and *cocktails_dag*).


## Note
This README is under construction, a lot of files for the Airflow are missing, in particular everything related to the ML training. This will be uploaded at a later date.
