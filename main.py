from fastapi import FastAPI
from backend.api.inference.model import model_api as model
from backend.config.schedule_conn import start_scheduler
from backend.api.schedule import schedule_api as schedule
from backend.api.inference.dataset import dataset_api as dataset

app = FastAPI()
app.include_router(model.router)
app.include_router(schedule.router)
app.include_router(dataset.router)

@app.get("/")
async def root():
    return {"message": "FastAPI - Inference server"}

@app.on_event("startup")
async def startup_event():
    start_scheduler(5)
    print("Scheduler start")
