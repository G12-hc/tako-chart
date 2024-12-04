from fastapi import APIRouter, HTTPException
from app.db import get_db_connection

router = APIRouter()

@router.get("/large")
def get_large_files(threshold: int = 1000):
    query = "SELECT * FROM files WHERE line_count > %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (threshold,))
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
