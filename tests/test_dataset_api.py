import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, ANY
from main import app
import os

client = TestClient(app)


# 테스트용 모델
class MockImageName:
    def __init__(self, image_name):
        self.image_name = image_name


# upload_dataset 테스트
@patch('backend.api.dataset_api.upload_image_to_s3')  # Zenko에 업로드하는 함수 모킹
@patch('backend.api.dataset_api.zipfile.ZipFile')  # ZipFile 모킹하여 실제 파일을 열지 않게 처리
@patch('backend.api.dataset_api.os.path.exists')  # 파일 경로 존재 여부를 모킹
def test_upload_dataset(zipfile_mock, os_exists_mock, upload_image_mock):
    # 테스트 데이터
    test_image_name = "test_images.zip"
    test_file_path = os.path.join("backend", "sample_image", test_image_name)

    # 파일이 존재한다고 가정
    os_exists_mock.return_value = True

    # ZIP 파일 내 이미지 목록 모킹 (3개의 이미지 파일이 있다고 가정)
    zip_mock = MagicMock()
    zip_mock.namelist.return_value = ["image1.jpg", "image2.jpg", "image3.jpg"]
    zipfile_mock.return_value.__enter__.return_value = zip_mock

    # API 호출
    response = client.post("/upload-dataset", json={"image_name": test_image_name})

    # 예상한 결과 검증
    assert response.status_code == 200
    assert response.json() == {"message": "Dataset uploaded successfully"}

    # Zenko에 업로드 함수가 호출되었는지 검증 (각 이미지 파일을 업로드)
    upload_image_mock.assert_any_call("image-dataset", "images/image1.jpg", ANY)
    upload_image_mock.assert_any_call("image-dataset", "images/image2.jpg", ANY)
    upload_image_mock.assert_any_call("image-dataset", "images/image3.jpg", ANY)


# 파일이 없을 때 처리하는 테스트
@patch('backend.api.dataset_api.os.path.exists')  # 파일 경로 존재 여부를 모킹
def test_upload_dataset_file_not_found(os_exists_mock):
    # 파일이 없다고 가정
    os_exists_mock.return_value = False

    # API 호출
    response = client.post("/upload-dataset", json={"image_name": "non_existent_file.zip"})

    # 예상한 결과 검증
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}


# 업로드된 파일 목록을 가져오는 엔드포인트 테스트
@patch('backend.api.dataset_api.get_s3_client')  # S3 클라이언트 모킹
@patch('backend.api.dataset_api.s3_client.list_objects_v2')  # S3에서 파일 목록을 가져오는 함수 모킹
def test_get_uploaded_files(s3_list_objects_mock, get_s3_client_mock):
    # 모킹된 S3 응답 (파일 목록)
    s3_list_objects_mock.return_value = {
        'Contents': [
            {'Key': 'images/image1.jpg'},
            {'Key': 'images/image2.jpg'},
            {'Key': 'images/image3.jpg'}
        ]
    }

    # API 호출
    response = client.get("/uploaded-files")

    # 예상한 결과 검증
    assert response.status_code == 200
    assert response.json() == {"uploaded_files": ['images/image1.jpg', 'images/image2.jpg', 'images/image3.jpg']}


# S3에서 파일 목록을 가져올 때 오류 발생 테스트
@patch('backend.api.dataset_api.get_s3_client')  # S3 클라이언트 모킹
@patch('backend.api.dataset_api.s3_client.list_objects_v2')  # S3에서 파일 목록을 가져오는 함수 모킹
def test_get_uploaded_files_error(s3_list_objects_mock, get_s3_client_mock):
    # 모킹된 S3 응답에서 오류를 발생시킴
    s3_list_objects_mock.side_effect = Exception("S3 connection error")

    # API 호출
    response = client.get("/uploaded-files")

    # 예상한 결과 검증 (오류가 발생했으므로 500)
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching files: S3 connection error"}
