from fastapi import APIRouter

from app.db import db_connection
from app.db.queries import (
    query_commits_per_author,
    query_commit_dates,
    query_repos,
    query_functional_line_counts_per_file,
    query_line_counts_per_file,
)
from app.parsing_data import assign_repo_data

router = APIRouter()


@router.get("/repos")
def get_all_repos():
    with db_connection() as conn:
        repos = query_repos(conn)
        return {"repos": repos}


@router.post("/fetch-repo/{owner}/{repo}")
async def import_repo_data(owner, repo):
    await assign_repo_data(owner, repo)


@router.get("/chart-data/commit-dates/{repo_id}")
def get_commit_dates(repo_id):
    with db_connection() as conn:
        # Get only the date portion of datetimes (we don't care about the times for
        # this chart)
        return [{"date": d["date"].date()} for d in query_commit_dates(conn, repo_id)]


@router.get("/chart-data/commits-per-author/{repo_id}")
def get_commits_per_author(repo_id):
    with db_connection() as conn:
        return query_commits_per_author(conn, repo_id)


@router.get("/chart-data/line-counts-per-file/{repo_id}")
def get_line_counts_per_file(repo_id):
    with db_connection() as conn:
        return query_line_counts_per_file(conn, repo_id)


@router.get("/chart-data/functional-line-counts-per-file/{repo_id}")
def get_functional_line_counts_per_file(repo_id):
    with db_connection() as conn:
        return query_functional_line_counts_per_file(conn, repo_id)
