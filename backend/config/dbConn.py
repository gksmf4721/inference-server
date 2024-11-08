# db_conn.py
import pymysql

def get_connection():
    # DB 연결을 설정합니다.
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='n7532056@',
        db='fast',
        charset='utf8'
    )
    return conn

def get_cursor():
    # 커서를 반환합니다.
    conn = get_connection()
    return conn.cursor(), conn
