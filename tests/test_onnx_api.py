import shutil

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import patch
import os
from PIL import Image
import io

from backend.api.inference.onnx.OnnxController import inference_status
from main import app

client = TestClient(app)

import shutil
import os
from PIL import Image
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.api.inference.onnx.OnnxController import inference_status
from main import app

client = TestClient(app)

import os
import shutil
from PIL import Image
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.api.inference.onnx.OnnxController import inference_status
from main import app

client = TestClient(app)


# 이미지 예측 API 테스트
@patch('backend.config.onnxConn.predict_image')  # predict_image 함수 모킹
def test_predict(predict_image_mock):
    # 모킹된 함수가 반환할 가짜 결과 설정
    predict_image_mock.return_value = "fake_prediction_result"

    # 존재하는 이미지 경로 테스트
    image_name = "bear_sample.jpg"
    os.makedirs('backend/sample_image/', exist_ok=True)

    # 원본 이미지 경로
    original_image_path = 'backend/sample_image/bear_sample.jpg'

    # 원본 이미지가 없다면, 샘플 이미지를 생성하여 저장
    if not os.path.exists(original_image_path):
        img = Image.new('RGB', (100, 100), color=(255, 0, 0))  # 빨간색 100x100 크기 이미지 생성
        img.save(original_image_path)  # 경로에 이미지 저장

    # 백업 파일 경로
    backup_image_path = 'backend/sample_image/bear_sample_backup.jpg'

    # 원본 이미지가 존재하면 백업 이미지 생성 (백업을 별도로 저장할 필요 없음)
    shutil.copy(original_image_path, backup_image_path)

    try:
        # API 호출
        response = client.post("/predict", json={"image_name": image_name})
        assert response.status_code == 202
        response_json = response.json()
        assert "request_id" in response_json
        assert response_json["message"] == "Request accepted and processing"

        # 존재하지 않는 이미지 경로 테스트
        response = client.post("/predict", json={"image_name": "non_existent_image.jpg"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Image not found"}
    finally:
        # 테스트 후 원본 파일 덮어쓰기
        if os.path.exists(backup_image_path):
            shutil.copy(backup_image_path, original_image_path)
            os.remove(backup_image_path)  # 백업 파일 삭제


# 추론 결과 조회 API 테스트
@patch('backend.config.onnxConn.predict_image')  # predict_image 함수 모킹
def test_get_result(predict_image_mock):
    predict_image_mock.return_value = "fake_prediction_result"

    # 가짜 request_id 생성
    request_id = "RequestID5000"
    inference_status[request_id] = {"status": "completed", "result": "fake_prediction_result"}

    response = client.get(f"/predict/{request_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "completed", "result": "fake_prediction_result"}

    # 존재하지 않는 request_id로 조회 시 404 오류
    response = client.get("/predict/non_existent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Request ID not found"}

    # 처리 중인 상태
    inference_status[request_id]["status"] = "processing"
    response = client.get(f"/predict/{request_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "processing"}


# 조회할 내역 없으면 오류
# 추론 내역 조회 API 테스트
@patch('backend.config.dbConn.select')  # select 함수 모킹
def test_get_history(select_mock):
    select_mock.return_value = [{"request_id": "RequestID5000", "status": "completed"}]

    response = client.get("/history")
    assert response.status_code == 200
    assert "result" in response.json()
    assert len(response.json()["result"]) > 0

    # query 파라미터와 함께 호출
    response = client.get("/history", params={"request_id": "RequestID5000"})
    assert response.status_code == 200
    assert len(response.json()["result"]) > 0

# 추론 내역 삭제 API 테스트
@patch('backend.config.dbConn.delete')  # delete 함수 모킹
def test_delete_history(delete_mock):
    delete_mock.return_value = "Deletion successful"

    response = client.delete("/history/1")
    assert response.status_code == 200
    assert response.json() == {"status": "completed", "result": "Deletion successful"}
