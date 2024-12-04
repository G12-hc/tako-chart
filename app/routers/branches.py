from fastapi import HTTPException
from fastapi import APIRouter

from app.db import get_db_connection
from app.db.queries import query_branches

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/{repo_id}")
def get_branches(repo_id):
    with get_db_connection() as conn:
        return query_branches(conn, repo_id)
