from fastapi import HTTPException, APIRouter
from psycopg2.extras import RealDictCursor

from app.db import get_db_connection
from app.db.queries import query_repositories

router = APIRouter(prefix="/repositories", tags=["Repositories"])


@router.get("/{repo_id}")
def get_repository_stats(repo_id):
    with get_db_connection() as conn:
        return query_repositories(conn, repo_id)

