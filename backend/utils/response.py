from typing import Optional

# 공통 응답 구조
def generate_response(status: str, message: str, data: Optional[dict] = None):
    return {
        "status": status,
        "message": message,
        "data": data
    }