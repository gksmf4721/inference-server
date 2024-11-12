import zipfile
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import os
from backend.config.zenko_conn import upload_image_to_s3, create_bucket, get_s3_client
from backend.utils.response import generate_response

app = FastAPI()
router = APIRouter()

# 이미지 경로 받는 모델
class ImageName(BaseModel):
    image_name: str

# zenko 버킷 명
bucket_name = "image-dataset"


@router.on_event("startup")
async def startup_event():
    create_bucket(bucket_name)

# dataset 업로드
@router.post("/upload-dataset")
async def upload_dataset(request: ImageName):
    # 서버에 저장된 ZIP 파일 경로 설정
    zip_file_path = os.path.join("backend", "sample_image", request.image_name)

    # 파일 존재 여부 확인
    if not os.path.exists(zip_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # ZIP 파일을 열어 각 이미지 파일을 Zenko에 업로드
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for image_name in zip_ref.namelist():
            with zip_ref.open(image_name) as image_file:
                upload_image_to_s3(bucket_name, f"images/{image_name}", image_file)

    # 공통 응답 구조 사용
    return generate_response("success", "Dataset uploaded successfully")


# 업로드된 파일 목록을 가져오는 엔드포인트
@router.get("/uploaded-files")
async def get_uploaded_files():
    try:
        s3_client = get_s3_client()
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='images/')
        files = response.get('Contents', [])
        file_names = [file['Key'] for file in files]

        # 공통 응답 구조 사용
        return generate_response("success", "Files fetched successfully", {"uploaded_files": file_names})
    except Exception as e:
        # 공통 응답 구조 사용
        raise HTTPException(status_code=500, detail=generate_response("error", f"Error fetching files: {str(e)}"))