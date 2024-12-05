from fastapi import APIRouter

from app.db import get_db_connection
from app.db.queries import query_licenses

router = APIRouter(prefix="/licenses", tags=["Licenses"])

@router.get("/{repo_id}")
def get_branches(repo_id):
    with get_db_connection() as conn:
        return query_licenses(conn, repo_id)
