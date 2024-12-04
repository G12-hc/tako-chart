from idlelib import query

from fastapi import HTTPException, APIRouter, params
from app.db.queries import *
import app.models.commits
from app.db import get_db_connection
from app.models.commits import Commit
router = APIRouter(prefix="/commits", tags=["Commits"])

@router.get("/{repo_id}")
def get_commits(repo_id):
    with get_db_connection() as conn:
        return query_commit(conn, repo_id)



