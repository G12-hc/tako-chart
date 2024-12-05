from fastapi import APIRouter, HTTPException

from app.db import get_db_connection
from app.db.queries import query_files

router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/{repo_id}")
def get_large_files(threshold):
    with get_db_connection() as conn:
        return query_files(conn, threshold)