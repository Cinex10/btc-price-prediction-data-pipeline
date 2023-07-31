from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
from tasks.data_collection import collect_data
from tasks.data_preprocess import preprocess_data
from tasks.evaluation import evaluate_model
from tasks.monitoring import monitor_model
from tasks.training import train_model

dag = DAG(
    dag_id='btc_price_data_pipeline',
    schedule_interval='@daily',
    start_date=pendulum.datetime(2023,7,22),
    catchup=False
)

t1 = PythonOperator(
    task_id='collect_data',
    python_callable=collect_data,
    op_args='e',
    dag=dag,
)

# t2 = PythonOperator(
#     task_id='preprocess_data',
#     python_callable=preprocess_data,
#     dag=dag,
# )

# t3 = PythonOperator(
#     task_id='train_model',
#     python_callable=train_model,
#     dag=dag,
# )

# t4 = PythonOperator(
#     task_id='evaluate_model',
#     python_callable=evaluate_model,
#     dag=dag,
# )

# # t5 = PythonOperator(
# #     task_id='deploy_model',
# #     python_callable=deploy_model,
# #     dag=dag,
# # )

# t6 = PythonOperator(
#     task_id='monitor_model',
#     python_callable=monitor_model,
#     dag=dag,
# )

t1

# t1 >> t2 >> t3 >> t4 >> t5 >> t6


    # get data
    # preprocess data
    # compare with real data
    # retrain