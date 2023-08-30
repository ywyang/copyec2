from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from huaweicloudECSDiscovery.servers import ECSServer


default_args = {
    'owner': 'devil.liu',  # 拥有者名称
    'start_date': datetime(2022, 12, 10, 12, 12),
    'provide_context': True,
}


ecs_discovery_dag = DAG(
    dag_id='ecs-discovery',  # dag_id
    default_args=default_args,  # 指定默认参数
    schedule_interval="0/30 * * * *",  # 执行周期，依次是分，时，日，月，年
)

region_list = Variable.get('HUAWEICLOUD_REGION_ID_LIST')


def ecs_discovery(region_id: str):
    ecs_server = ECSServer(region_id=region_id)
    ecs_server.discovery(limit=100)


for region_id in region_list.split(","):

    _ = PythonOperator(
        task_id=f"{region_id}-discovery-task",
        python_callable=ecs_discovery,
        dag=ecs_discovery_dag,
        op_kwargs={
            "region_id": region_id
        }
    )