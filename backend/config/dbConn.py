from datetime import datetime
from typing import Optional

from numpy import double
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("mysql+pymysql://root:n7532056%40@localhost/fast")
Session = sessionmaker(bind=engine)


class Inference(Base):
    __tablename__ = "inference"
    IDX = Column(Integer, primary_key=True, index=True)
    REQUEST_ID = Column(String)
    PROCESS_TIME = Column(DateTime, default=datetime.utcnow)
    FILE_PATH = Column(String)
    RESULT_DATA = Column(String)
    RUNTIME = Column(DOUBLE)

def insert(request_id: str, image_path: str, result_data: str, runtime_seconds: double):
    session = Session()
    try:
        insert_query = Inference(
            REQUEST_ID=request_id,
            FILE_PATH=image_path,
            RESULT_DATA=result_data,
            RUNTIME=runtime_seconds
        )
        session.add(insert_query)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


def select(request_id: Optional[str] = None,
           process_time: Optional[datetime] = None,
           pagination: Optional[int] = None,
           runtime: Optional[float] = None):
    session = Session()
    select_query = session.query(Inference).order_by(Inference.IDX)  # 기본 쿼리

    if request_id:
        select_query = select_query.filter(Inference.REQUEST_ID == request_id)
    if process_time:
        select_query = select_query.filter(Inference.PROCESS_TIME == process_time)
    if runtime:
        select_query = select_query.filter(Inference.RUNTIME <= runtime)  # 예시: RUNTIME이 주어진 값 이하일 때
    if pagination:
        select_query = select_query.limit(pagination)

    result = select_query.all()

    return result


def delete(idx: int):
    session = Session()
    try:
        delete_query = session.query(Inference).filter(Inference.IDX == idx)
        delete_query.delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print("Not Found Index")
    finally:
        session.close()


def delete_old_records():
    session = Session()
    # 가장 오래된 레코드(인덱스 기준이 아닌 ID나 생성일 기준)부터 삭제
    oldest_record = session.query(Inference).order_by(Inference.IDX).first()  # 가장 오래된 레코드 조회
    if oldest_record:
        session.delete(oldest_record)
        session.commit()
    session.close()
