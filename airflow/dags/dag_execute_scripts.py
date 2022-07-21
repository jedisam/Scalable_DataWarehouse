import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
