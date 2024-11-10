# import threading
#
# from fastapi import APIRouter, FastAPI
# from backend.config.scheduleConn import start_scheduler, cancel_scheduler
# app = FastAPI()
# router = APIRouter()
#
# job_thread = None
# stop_event = threading.Event()
#
# # 스케줄링 주기 조정
# @app.post("/schedule")
# async def schedule(cycle: int):
#     from backend.config.scheduleConn import cancel_scheduler
#     cancel_scheduler()  # Cancel any existing job before starting a new one
#     stop_event.clear()  # Reset stop event
#     job_thread = threading.Thread(target=start_scheduler, args=(cycle,), daemon=True)
#     job_thread.start()
#     return {"status": "scheduler started", "cycle": cycle}
