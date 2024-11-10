from datetime import datetime
from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from numpy import double
from pydantic import BaseModel
import os
from typing_extensions import Optional
from backend.config.onnxConn import predict_image
from backend.config.dbConn import select, delete

app = FastAPI()
router = APIRouter()


# 이미지 경로 받는 모델
class ImageName(BaseModel):
    image_name: str


# 요청 상태를 저장하는 딕셔너리
inference_status = {}


# 예측 비동기 작업
async def process_request(request_id: str, image_path: str, start_time: datetime):
    result = predict_image(request_id, image_path, start_time)
    inference_status[request_id] = {"status": "completed", "result": result}


@router.post("/predict", status_code=202)
async def predict(request: ImageName, background_tasks: BackgroundTasks):
    start_time = datetime.now()

    image_path = os.path.join("backend", "sample_image", request.image_name)

    # 이미지 경로가 존재하는지 확인
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # 작업 ID 생성 및 상태 저장
    # request_id = str(uuid.uuid4())
    request_id = "RequestID5000"

    inference_status[request_id] = {"status": "processing"}

    # 비동기 작업으로 예측 처리 시작
    background_tasks.add_task(process_request, request_id, image_path, start_time)

    return {"request_id": request_id, "message": "Request accepted and processing"}


@router.get("/predict/{request_id}")
async def get_result(request_id: str):
    # 작업 ID 상태 확인
    if request_id not in inference_status:
        raise HTTPException(status_code=404, detail="Request ID not found")

    # 작업 완료 여부 확인
    status_info = inference_status[request_id]
    if status_info["status"] == "processing":
        return {"status": "processing"}

    # 작업 완료 시 결과 반환
    return {"status": "completed", "result": status_info["result"]}


# 추론 내역 조회
@router.get("/history")
async def get_history(request_id: Optional[str] = None,
                      process_time: Optional[datetime] = None,
                      pagination: Optional[int] = None,
                      runtime: Optional[float] = None):
    result = select(request_id, process_time, pagination, runtime)
    return {"result" : result}


# 추론 내역 삭제
@router.delete("/history/{idx}")
async def delete_history(idx: int):
    result = delete(idx)
    return {"status": "completed", "result": result}