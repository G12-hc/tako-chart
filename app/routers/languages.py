from fastapi import HTTPException, APIRouter

from app.db import get_db_connection
from app.db.queries import query_languages, query_licenses

router = APIRouter(prefix="/repo_data")
@router.get("/{repo_id}")
def get_large_files(repo_id):
    with get_db_connection() as conn:
        languages = query_languages(conn, repo_id)
        licenses = query_licenses(conn, repo_id)
        return {"languages": languages, "licenses": licenses}


