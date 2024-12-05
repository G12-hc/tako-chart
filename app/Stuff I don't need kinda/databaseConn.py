from fastapi import FastAPI, Query, HTTPException
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

# PostgreSQL connection function with a context manager
def get_db_connection():
    return connect(
        dbname="HackCamp",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

# Pydantic models for response schemas
class Commit(BaseModel):
    id: int
    author: str
    date: str
    message: str

class File(BaseModel):
    id: int
    name: str
    line_count: int

class RepositoryStats(BaseModel):
    commit_count: int
    branch_count: int
    file_count: int

@app.get("/commits", response_model=List[Commit])
def fetch_commits(
    author: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    query = "SELECT * FROM commits WHERE TRUE"
    params = []
    if author:
        query += " AND author = %s"
        params.append(author)
    if start_date and end_date:
        query += " AND date BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, tuple(params))
            commits = cursor.fetchall()
        return commits
    finally:
        conn.close()

@app.get("/files/large", response_model=List[File])
def large_files(threshold: int = Query(1000)):
    query = "SELECT * FROM files WHERE line_count > %s"

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (threshold,))
            files = cursor.fetchall()
        return files
    finally:
        conn.close()

@app.get("/repositories/{repo_id}/stats", response_model=RepositoryStats)
def repo_stats(repo_id: int):
    query = """
    SELECT
        (SELECT COUNT(*) FROM commits WHERE repository_id = %s) AS commit_count,
        (SELECT COUNT(*) FROM branches WHERE repository_id = %s) AS branch_count,
        (SELECT COUNT(*) FROM files WHERE branch_id IN (SELECT id FROM branches WHERE repository_id = %s)) AS file_count
    """

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (repo_id, repo_id, repo_id))
            stats = cursor.fetchone()
        if not stats:
            raise HTTPException(status_code=404, detail="Repository not found")
        return stats
    finally:
        conn.close()
