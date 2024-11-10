import threading
import schedule
import time
from functools import partial

# job_instance = None
# stop_event = threading.Event()
#
# def test_job(cycle):
#     print(f"Job running with cycle {cycle}")
#
# def start_scheduler(cycle: int):
#     global job_instance, stop_event
#     if job_instance:
#         schedule.cancel_job(job_instance)
#
#     job_instance = schedule.every(cycle).seconds.do(partial(test_job, cycle))
#
#     while not stop_event.is_set():
#         schedule.run_pending()
#         time.sleep(1)
#
# def cancel_scheduler():
#     global stop_event, job_instance
#     if job_instance:
#         print("Cancelling existing job...")
#         schedule.cancel_job(job_instance)
#         job_instance = None
#     stop_event.set()
#     print("Job cancelled.")
