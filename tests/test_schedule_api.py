import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# 스케줄링 작업 추가 API 테스트
@patch('backend.config.scheduler.scheduler.get_job')
@patch('backend.config.scheduler.scheduler.remove_job')
@patch('backend.config.scheduler.scheduler.start')
@patch('backend.config.scheduler.start_scheduler')
def test_schedule(start_scheduler_mock, scheduler_start_mock, scheduler_remove_mock, scheduler_get_mock):
    # 스케줄러에서 가져오는 작업이 없다고 설정
    scheduler_get_mock.return_value = None

    # 새 작업을 추가하는 동작을 모킹 (실제 함수 동작을 방지)
    start_scheduler_mock.return_value = None

    # 기존 작업이 있는지 확인
    scheduler_get_mock.return_value = None  # 기존 작업이 없다고 설정

    # API 호출 (스케줄링 요청)
    response = client.post("/schedule", json={"cycle": "daily"})

    # 예상 결과 검증
    assert response.status_code == 200
    assert response.json() == {"result": "Scheduled task added successfully."}

    # 작업 제거 함수가 호출된 부분 검증
    scheduler_remove_mock.assert_called_once_with("remove_inference")

    # 새 작업을 추가하는 함수가 호출된 부분 검증
    start_scheduler_mock.assert_called_once_with("daily")

    # 스케줄러가 시작된 상태 확인
    scheduler_start_mock.assert_called_once()


# 기존 작업이 있을 때 삭제하고 새 작업 추가
@patch('backend.config.scheduler.scheduler.get_job')
@patch('backend.config.scheduler.scheduler.remove_job')
@patch('backend.config.scheduler.scheduler.start')
@patch('backend.config.scheduler.start_scheduler')
def test_schedule_with_existing_job(start_scheduler_mock, scheduler_start_mock, scheduler_remove_mock,
                                    scheduler_get_mock):
    # 기존 작업이 존재한다고 설정 (기존 작업을 제거하는 부분 검증)
    scheduler_get_mock.return_value = MagicMock()

    # API 호출 (스케줄링 요청)
    response = client.post("/schedule", json={"cycle": "hourly"})

    # 예상 결과 검증
    assert response.status_code == 200
    assert response.json() == {"result": "Scheduled task added successfully."}

    # 작업 제거 함수가 호출된 부분 검증 (기존 작업이 제거됨)
    scheduler_remove_mock.assert_called_once_with("remove_inference")

    # 새 작업을 추가하는 함수가 호출된 부분 검증
    start_scheduler_mock.assert_called_once_with("hourly")

    # 스케줄러가 시작된 상태 확인
    scheduler_start_mock.assert_called_once()


# 스케줄러가 이미 실행 중일 때
@patch('backend.config.scheduler.scheduler.get_job')
@patch('backend.config.scheduler.scheduler.remove_job')
@patch('backend.config.scheduler.scheduler.start')
@patch('backend.config.scheduler.start_scheduler')
def test_schedule_when_scheduler_is_running(start_scheduler_mock, scheduler_start_mock, scheduler_remove_mock,
                                            scheduler_get_mock):
    # 스케줄러가 이미 실행 중인 상태로 설정
    scheduler_get_mock.return_value = None
    scheduler_start_mock.return_value = None

    # API 호출 (스케줄링 요청)
    response = client.post("/schedule", json={"cycle": "weekly"})

    # 예상 결과 검증
    assert response.status_code == 200
    assert response.json() == {"result": "Scheduled task added successfully."}

    # 기존 작업 제거가 호출되었는지 확인
    scheduler_remove_mock.assert_called_once_with("remove_inference")

    # 새 작업을 추가하는 함수 호출 확인
    start_scheduler_mock.assert_called_once_with("weekly")

    # 스케줄러 시작은 호출되지 않음 (이미 실행 중이므로)
    scheduler_start_mock.assert_not_called()
