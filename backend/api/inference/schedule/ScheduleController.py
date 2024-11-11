from apscheduler.jobstores.base import JobLookupError

from fastapi import APIRouter, FastAPI

from backend.config.scheduleConn import scheduler, start_scheduler, Schedule

app = FastAPI()
router = APIRouter()




# 스케줄링 주기 조정
# 스케줄링 주기 조정
@router.post("/schedule")
async def schedule(s: Schedule):
    cycle = s.cycle
    print(f"Cycle: {cycle}")

    # 기존 작업이 있으면 제거
    job = scheduler.get_job("remove_inference")
    if job:
        scheduler.remove_job("remove_inference")
        print("Removed existing job.")

    # 스케줄러가 실행 중인 상태인지 확인하고, 필요 시 시작
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started.")

    try:
        # 새 작업 추가
        start_scheduler(cycle)  # 새 작업을 추가하는 함수
        print("New scheduled task started.")
        return {"result": "Scheduled task added successfully."}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}

