from fastapi import APIRouter, HTTPException
from app.db import get_db_connection

router = APIRouter()

@router.get("/{repo_id}")
def get_branches(repo_id: int):
    query = "SELECT * FROM branches WHERE repository_id = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (repo_id,))
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
