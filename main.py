import threading

from fastapi import FastAPI
from backend.api.inference.onnx import OnnxController as onnx
# from backend.config.scheduleConn import start_scheduler
# from backend.api.inference.schedule import ScheduleController as schedule

app = FastAPI()
app.include_router(onnx.router)
# app.include_router(schedule.router)

job_thread = None
stop_event = threading.Event()
@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.on_event("startup")
# def startup():
#     global job_thread, stop_event
#     if job_thread is None or not job_thread.is_alive():
#         stop_event.clear()  # Reset event
#         job_thread = threading.Thread(target=start_scheduler, args=(5,), daemon=True)
#         job_thread.start()
