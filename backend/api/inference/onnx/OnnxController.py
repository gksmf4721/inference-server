from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from backend.config.onnxConn import predict_image
import os

app = FastAPI()
router = APIRouter()

# 이미지 경로 받는 모델
class ImageName(BaseModel):
    image_name: str

@router.post("/predict")
async def predict(request: ImageName):

    image_path = os.path.join("backend", "sample_image", request.image_name)
    print(image_path)


    absolute_image_path = os.path.abspath(image_path)
    print(f"Absolute image path: {absolute_image_path}")


    # 이미지 경로가 존재하는지 확인
    if not os.path.exists(image_path):
        return {"error": "Image file not found"}

    result = predict_image(image_path)

    return {"result": str(result)}

