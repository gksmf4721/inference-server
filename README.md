**<h1>FastAPI (Inference-Server)</h1>**

<br>

---
🔗[Notion Link] [FastAPI Project (Inference-Server)](https://www.notion.so/FastAPI-Project-Inference-Server-1369e3d7efed805d8664d14a9676fb2e?pvs=21)
<br>🔗[Github Link] https://github.com/gksmf4721/inference-server
---
### 🚀 프로젝트 소개

FastAPI를 활용하여 ONNX와 TFLite 모델 기반의 이미지 분류(CV) API 서버를 구축하고, 추론 이력 조회와 삭제 기능을 제공하는 시스템입니다.<br>
다양한 사용자 요청을 효율적으로 관리하기 위해 큐와 스케줄링을 도입하고, 대용량 데이터 처리를 위해 오브젝트 스토리지를 구성했습니다.

---

### 🚀 환경

1. **IDE:** PyCharm
2. **Framework:** FastAPI
3. **Language:** Python 3.12
4. **Interpreter:** venv (기본 내장)
5. **Model:** ONNX, Tensorflow Lite
6. **Database:** MariaDB

---

### 🚀 폴더 및 파일 구조와 기능

- **[API]** - `/backend/api`
    - `/inference/dataset/dataset_api.py`: 데이터셋 업로드 및 다중 이미지 추론 처리 API.
    - `/inference/model/model_api.py`: ONNX 및 TFLite 모델 기반의 단일 이미지 분류 API.
    - `/schedule/schedule_api.py`: 추론 기록 삭제 주기를 설정하는 API.
- **[Config]** - `/backend/config`
    - `db_conn.py`: MariaDB 데이터베이스 연결 설정.
    - `onnx_conn.py`: ONNX 모델 로드 및 추론 설정.
    - `tflite_conn.py`: TFLite 모델 로드 및 추론 설정.
    - `schedule_conn.py`: 스케줄러 설정 (apscheduler 사용).
    - `zenko_conn.py`: Zenko 오브젝트 스토리지 연결 설정.
- **[Schema]** - `/doc/db`
    - `schema.sql`: MariaDB 스키마 정의 파일.
- **[Models]** - `/backend/models`
    - ONNX 모델 파일 및 TFLite 모델 파일 포함.
        - `classification_mobilenet_v3_small_best.onnx`
        - `classification_mobilenet_v3_small_best.tflite`
- **[Utils]** - `/backend/utils`
    - `response.py`: API 응답 형식 관련 유틸리티 파일.
- **[Sample image]** - `/backend/sample_image`
    - 테스트용 샘플 이미지 파일.
- **[Test]** - `/tests`
    - `test_dataset_api.py`: 데이터셋 API 테스트.
    - `test_model_api.py`: 모델 API 테스트.
    - `test_schedule_api.py`: 스케줄 API 테스트.

---

### 🚀 주요 API 기능

1. **단일 이미지 추론 API**
    - ONNX 및 TFLite 모델을 통해 단일 이미지를 분류하고 결과를 반환.
    - 입력: 이미지 파일 (jpg, png)
    - 출력: 이미지 분류 결과 클래스
    - 다중 사용자 요청을 큐로 관리하여 효율적으로 분배 및 처리.
2. **Inference 이력 조회 API**
    - 추론 이력을 시간, 페이지네이션, 런타임, 사용자 요청 ID를 기반으로 조회.
    - 복합 검색 기능으로 조건별 조회 가능.
3. **Inference 이력 삭제 API**
    - 특정 추론 기록을 삭제하는 API.
4. **대용량 이미지 데이터 추론 API**
    - Zenko 오브젝트 스토리지에 대용량 데이터 업로드 및 다중 이미지 추론 지원.
    - 다양한 이미지 형식(.jpg, .jpeg, .png) 포함한 zip 파일 업로드 환경 구축.
    - run 명령어
        
        ```bash
        docker run -d --name cloudserver -p 8000:8000 -e SCALITY_ACCESS_KEY_ID=test_access -e SCALITY_SECRET_ACCESS_KEY=test_secret -e REMOTE_MANAGEMENT_DISABLE=1 zenko/cloudserver
        ```
        
5. **주기적 Inference 이력 삭제 프로세스**
    - 스케줄러(apscheduler)를 사용하여 일정 주기로 Inference 이력을 삭제.
    - 삭제 주기를 설정할 수 있는 API 제공.

### 🚀 기타 구현 사항

- **단위 테스트**: 각 API 기능에 대한 단위 테스트 작성으로 기능 검증.
- **추론 이력 관리**: MariaDB, SQLAlchemy를 활용하여 이력 데이터베이스 관리.



