from airflow.providers.standard.operators.python import PythonOperator


# # 真实温度读取（Linux示例）
# def get_real_temperature():
#     # from sensors import Sensors
#     return "get_real_temperature"
#
# def generate_report():
#     import matplotlib.pyplot as plt
#     # 生成温度曲线图
#     # 保存到Airflow的logs目录
#     return "generate_report"
#

from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
from airflow.exceptions import AirflowException
from datetime import datetime
import time
import subprocess
import random
import os

# 共享文件路径定义
ABORT_FLAG_PATH = '/tmp/abort_flag'
TEMP_LOG_PATH = '/tmp/temperature.log'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0
}


def set_abort_flag():
    with open(ABORT_FLAG_PATH, 'w') as f:
        f.write('1')


def check_abort_flag():
    return os.path.exists(ABORT_FLAG_PATH)


def cleanup():
    for path in [ABORT_FLAG_PATH, TEMP_LOG_PATH]:
        if os.path.exists(path):
            os.remove(path)


def pressure_test(**kwargs):
    cleanup()  # 清理旧标志
    proc = subprocess.Popen("stress-ng --cpu 4 --timeout 300", shell=True)

    try:
        while proc.poll() is None:
            if check_abort_flag():
                proc.terminate()
                raise AirflowException("压力测试因异常终止")
            time.sleep(1)

        if proc.returncode != 0:
            raise AirflowException("压力测试失败")
    finally:
        proc.terminate()


def read_temperature(**kwargs):
    while True:
        # 模拟温度读取（实际应替换为真实传感器读取逻辑）
        temp = random.randint(30, 100)
        with open(TEMP_LOG_PATH, 'a') as f:
            f.write(f"{datetime.now()},{temp}\n")

        if check_abort_flag():
            raise AirflowException("温度记录因异常终止")

        time.sleep(1)


def monitor_temperature(**kwargs):
    while True:
        time.sleep(1)

        if not os.path.exists(TEMP_LOG_PATH):
            continue

        with open(TEMP_LOG_PATH, 'r') as f:
            lines = f.readlines()
            if lines:
                last_temp = float(lines[-1].split(',')[1])
                if last_temp > 80:  # 温度阈值设为80度
                    set_abort_flag()
                    raise AirflowException(f"温度异常！当前温度：{last_temp}℃")


with DAG(
        'system_stress_test',
        default_args=default_args,
        schedule_interval=None,
        catchup=False,
        on_success_callback=lambda _: cleanup(),
        on_failure_callback=lambda _: cleanup()
) as dag:
    pressure_task = PythonOperator(
        task_id='run_stress_test',
        python_callable=pressure_test,
        trigger_rule='all_success'
    )

    temp_log_task = PythonOperator(
        task_id='log_temperature',
        python_callable=read_temperature
    )

    monitor_task = PythonOperator(
        task_id='monitor_temperature',
        python_callable=monitor_temperature
    )

    [pressure_task, temp_log_task] >> monitor_task