import threading
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel
from backend.config.db_conn import delete_old_records

job_instance = None
stop_event = threading.Event()

scheduler = BackgroundScheduler()

class Schedule(BaseModel):
    cycle: int

def scheduled_task(cycle: int):
    print(f"Test Cycle : {cycle}")
    # 오래된 레코드 삭제 함수 (원활한 테스트를 위해 주석 처리)
    # delete_old_records()

def start_scheduler(cycle: int):
    scheduler.add_job(scheduled_task, 'interval', seconds=cycle, id="remove_inference", args=(cycle,))  # 10초마다 실행
    scheduler.start()
