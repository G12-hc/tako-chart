from fastapi import APIRouter
from app.db import get_db_connection
from app.db.queries import query_repos

router = APIRouter(prefix="/repos")


@router.get("/")
def get_all_repos():
    conn = get_db_connection()
    repos = query_repos(conn)
    return {"repos": repos}
