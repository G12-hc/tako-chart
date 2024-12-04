from fastapi import APIRouter, HTTPException
from app.db import get_db_connection

router = APIRouter()

@router.get("/{repo_id}")
def get_license(repo_id: int):
    query = "SELECT * FROM licenses WHERE id = (SELECT license_id FROM repositories WHERE id = %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (repo_id,))
            return cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
