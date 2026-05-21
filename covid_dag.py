import json
import logging
import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.io as pio





def fetch_covid_file(ti):
    df = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/5c4e1452-3850-4b59-b11c-3dd51d7fb8b5")
    now = datetime.now().strftime(format = "%Y_%m_%d_%H_%M_%S")
    filename = now + '.csv'
    df.to_csv(f"./data/{filename}", index=False)
    ti.xcom_push(key="filename", value=filename)


def generate_image(ti):
    # Get filename from XCom
    filename = ti.xcom_pull(task_ids="fetch_covid_file", key="filename")
    file_source = f"./data/{filename}"
    
    df = pd.read_csv(file_source)
    data = df.groupby(by = 'date').incid_hosp.mean().to_frame(name = 'mean_incid_hosp').reset_index()
    fig = px.line(data, x='date', y="mean_incid_hosp")
    image_name = filename.replace('.csv', '.png')

    pio.orca.config.use_xvfb = True
    fig.write_image(f"./data/{image_name}" , engine='orca')



with DAG("covid_dag", start_date=datetime(2022, 1, 1), schedule="@daily", catchup=False) as dag:
    
    fetch_covid_file_task = PythonOperator(
        task_id="fetch_covid_file", 
        python_callable=fetch_covid_file
    )
    
    generate_image_task = PythonOperator(
        task_id="generate_image", 
        python_callable=generate_image
    )

    fetch_covid_file_task >> generate_image_task
