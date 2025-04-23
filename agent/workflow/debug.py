import os
import random
import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

# 共享配置
ABORT_FLAG_PATH = '/tmp/abort_flag'
TEMP_LOG_PATH = '/tmp/temperature.log'
RUN_DURATION = 7200  # 2小时（秒）
RUN_DURATION = 100  # 2小时（秒）

# 进程管理器
processes = {}


def set_abort_flag():
    with open(ABORT_FLAG_PATH, 'w') as f:
        f.write('1')


def check_abort_flag():
    return os.path.exists(ABORT_FLAG_PATH)


def cleanup():
    """清理资源和终止进程"""
    for path in [ABORT_FLAG_PATH, TEMP_LOG_PATH]:
        if os.path.exists(path):
            os.remove(path)

    # 终止所有子进程
    for name, proc in processes.items():
        if proc.poll() is None:
            proc.terminate()
            print(f"Terminated {name}")


def execute_with_duration(func, duration, *args, **kwargs):
    """带超时控制的执行装饰器"""
    start_time = time.time()
    while time.time() - start_time < duration:
        if check_abort_flag():
            raise AirflowException("任务被异常终止")
        func(*args, **kwargs)
    return True


def pressure_test(**kwargs):
    """压力测试任务"""
    print("pressure_test")
    # cleanup()
    # cmd = "stress-ng --cpu 4 --timeout {}".format(RUN_DURATION)
    # processes['stress'] = subprocess.Popen(
    #     cmd, shell=True, preexec_fn=os.setsid
    # )
    #
    # try:
    #     processes['stress'].wait()
    #     if processes['stress'].returncode != 0:
    #         raise AirflowException("压力测试失败")
    # except:
    #     os.killpg(os.getpgid(processes['stress'].pid), signal.SIGTERM)
    #     raise


def read_temperature(**kwargs):
    """温度记录任务"""

    def _read_task():
        temp = random.randint(30, 100)  # 模拟温度
        with open(TEMP_LOG_PATH, 'a') as f:
            f.write(f"{datetime.now().isoformat()},{temp}\n")
        time.sleep(1)

    execute_with_duration(_read_task, RUN_DURATION)


def monitor_temperature(**kwargs):
    """温度监控任务"""

    def _monitor_task():
        if not os.path.exists(TEMP_LOG_PATH):
            return

        with open(TEMP_LOG_PATH, 'r') as f:
            lines = f.readlines()
            if lines:
                last_temp = float(lines[-1].split(',')[1])
                if last_temp > 80:  # 阈值
                    set_abort_flag()
                    raise AirflowException(f"温度异常！当前温度：{last_temp}℃")
        time.sleep(5)

    try:
        execute_with_duration(_monitor_task, RUN_DURATION)
    except AirflowException as e:
        raise e


with DAG(
        'enhanced_stress_test',
        default_args={
            'owner': 'airflow',
            # 'start_date': datetime(2023, 1, 1),
            'retries': 0
        },
        schedule_interval=None,
        catchup=False,
        dagrun_timeout=timedelta(seconds=RUN_DURATION + 300),
        on_success_callback=lambda _: cleanup(),
        on_failure_callback=lambda _: cleanup()
) as dag:
    pressure_task = PythonOperator(
        task_id='pressure_test',
        python_callable=pressure_test
    )

    temp_task = PythonOperator(
        task_id='temperature_logging',
        python_callable=read_temperature
    )

    monitor_task = PythonOperator(
        task_id='temperature_monitoring',
        python_callable=monitor_temperature
    )

    task = BashOperator(
        task_id='example_task',
        bash_command='echo "Hello, World!"',
        retries=3,
        retry_delay=timedelta(minutes=5)
    )

    [pressure_task, temp_task, monitor_task] >> task
