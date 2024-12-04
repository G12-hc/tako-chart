from fastapi import HTTPException, APIRouter

from app.db import get_db_connection
from app.db.queries import query_languages

router = APIRouter(prefix="/languages", tags=["Languages"])
@router.get("/{repo_id}")
def get_large_files(repo_id):
    with get_db_connection() as conn:
        return query_languages(conn, repo_id)