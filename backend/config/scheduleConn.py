import threading
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel
from backend.config.dbConn import delete_old_records

job_instance = None
stop_event = threading.Event()

scheduler = BackgroundScheduler()


class Schedule(BaseModel):
    cycle: int


def scheduled_task(cycle: int):
    print(f"Scheduled task is running atttt : {cycle}")
    # delete_old_records()

def start_scheduler(cycle: int):
    scheduler.add_job(scheduled_task, 'interval', seconds=cycle, id="remove_inference", args=(cycle,))  # 10초마다 실행
    scheduler.start()
