from fastapi import APIRouter, FastAPI
from backend.config.schedule_conn import scheduler, start_scheduler, Schedule
from backend.utils.response import generate_response

app = FastAPI()
router = APIRouter()

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
        return generate_response("success", "Scheduled task added successfully.")
    except Exception as e:
        return generate_response("error", f"Error: {str(e)}")

