from fastapi import APIRouter, HTTPException
from app.db import get_db_connection

router = APIRouter()


@router.get("/")
def get_commits(author: str = None, start_date: str = None, end_date: str = None):
    query = "SELECT * FROM commits WHERE TRUE"
    params = []
    if author:
        query += " AND author = %s"
        params.append(author)
    if start_date and end_date:
        query += " AND date BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
