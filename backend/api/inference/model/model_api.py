from datetime import datetime
from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
from typing_extensions import Optional
from backend.config.onnx_conn import onnx_predict_image
from backend.config.db_conn import select, delete
from backend.config.tflite_conn import tflite_predict_image
from backend.utils.response import generate_response

app = FastAPI()
router = APIRouter()

# 이미지 경로 받는 모델
class ImageName(BaseModel):
    image_name: str

# 요청 상태를 저장하는 딕셔너리
inference_status = {}

# 공통된 비동기 예측 처리 함수
async def process_request(request_id: str, image_path: str, start_time: datetime, prediction_function):
    result = prediction_function(request_id, image_path, start_time)
    inference_status[request_id] = {"status": "completed", "result": result}

# 공통된 이미지 경로 확인 및 상태 설정 함수
def setup_request(request: ImageName, model_name: str):
    image_path = os.path.join("backend", "sample_image", request.image_name)

    # 이미지 경로가 존재하는지 확인
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # 작업 ID 생성 및 상태 저장
    request_id = f"RequestID_{model_name}"

    inference_status[request_id] = {"status": "processing"}

    return image_path, request_id

# ONNX 이미지 추론 실행
@router.post("/onnx/predict", status_code=202)
async def predict_onnx(request: ImageName, background_tasks: BackgroundTasks):
    start_time = datetime.now()
    image_path, request_id = setup_request(request, "onnx")

    # 비동기 작업으로 예측 처리 시작
    background_tasks.add_task(process_request, request_id, image_path, start_time, onnx_predict_image)

    return generate_response("processing", "Request accepted and processing", {"request_id": request_id})

# TFLite 예측 실행
@router.post("/tflite/predict", status_code=202)
async def predict_tflite(request: ImageName, background_tasks: BackgroundTasks):
    start_time = datetime.now()
    image_path, request_id = setup_request(request, "tflite")

    # 비동기 작업으로 예측 처리 시작
    background_tasks.add_task(process_request, request_id, image_path, start_time, tflite_predict_image)

    return generate_response("processing", "Request accepted and processing", {"request_id": request_id})

# 추론 결과 반환
@router.get("/predict/{request_id}")
async def get_result(request_id: str):
    # 작업 ID 상태 확인
    if request_id not in inference_status:
        raise HTTPException(status_code=404, detail="Request ID not found")

    # 작업 완료 여부 확인
    status_info = inference_status[request_id]
    if status_info["status"] == "processing":
        return generate_response("processing", "Request is being processed")

    # 작업 완료 시 결과 반환
    return generate_response("completed", "Request completed successfully", {"result": status_info["result"]})

# 추론 내역 조회
@router.get("/history")
async def get_history(request_id: Optional[str] = None,
                      process_time: Optional[datetime] = None,
                      pagination: Optional[int] = None,
                      runtime: Optional[float] = None):
    result = select(request_id, process_time, pagination, runtime)
    return generate_response("success", "History retrieved successfully", {"result": result})

# 추론 내역 삭제
@router.delete("/history/{idx}")
async def delete_history(idx: int):
    result = delete(idx)
    return generate_response("success", "History deleted successfully", {"result": result})
