from fastapi import APIRouter

from app.db.connection import get_db_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()
def get_repository_stats(repo_id: int):
    """
    Fetch repository statistics such as commit count, branch count, and file count.
    """
    query = """
    SELECT
        (SELECT COUNT(*) FROM commits WHERE repository_id = %s) AS commit_count,
        (SELECT COUNT(*) FROM branches WHERE repository_id = %s) AS branch_count,
        (SELECT COUNT(*) FROM files WHERE branch_id IN (
            SELECT id FROM branches WHERE repository_id = %s)) AS file_count
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (repo_id, repo_id, repo_id))
            stats = cursor.fetchone()
    return stats

