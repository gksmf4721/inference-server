from fastapi import FastAPI, APIRouter
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from backend.config.dbConn import get_cursor

app = FastAPI()

router = APIRouter()

# SQLAlchemy??Base ?대옒???앹꽦
Base = declarative_base()


# ?덉떆: Item 紐⑤뜽 ?뺤쓽
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

@router.get("/get")
async def get_items():
    cursor, conn = get_cursor()  # 而ㅼ꽌? ?곌껐 媛?몄삤湲?
    try:
        sql = 'SELECT * FROM test'
        cursor.execute(sql)
        result = cursor.fetchall()
        return {"result": result}
    finally:
        cursor.close()
        conn.close()  # ?곌껐???レ뒿?덈떎.