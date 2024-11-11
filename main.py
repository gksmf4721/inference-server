from fastapi import FastAPI
from backend.api.inference.onnx import OnnxController as onnx
from backend.config.scheduleConn import start_scheduler
from backend.api.inference.schedule import ScheduleController as schedule

app = FastAPI()
app.include_router(onnx.router)
app.include_router(schedule.router)

# job_thread = None
# stop_event = threading.Event()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    start_scheduler(5)
    print("Scheduler started with the app startup.")
