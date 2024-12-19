from fastapi import APIRouter

from app.db import db_connection
from app.db.queries import (
    query_commits_per_author,
    query_commit_dates,
    query_repos,
    query_functional_line_counts_per_file,
    query_line_counts_per_file,
    query_delete_all_repo_data,
)
from app.parsing_data import assign_repo_data

router = APIRouter()


@router.get("/repos")
async def get_all_repos():
    async with db_connection() as conn:
        repos = await query_repos(conn)
        return {"repos": repos}


@router.post("/repos/fetch/{owner}/{repo}")
async def import_repo_data(owner, repo):
    await assign_repo_data(owner, repo)


@router.delete("/repos/delete/{repo_id}")
async def delete_repo_data(repo_id):
    async with db_connection() as conn:
        await query_delete_all_repo_data(conn, repo_id)


@router.get("/chart-data/commit-dates/{repo_id}")
async def get_commit_dates(repo_id):
    async with db_connection() as conn:
        # Get only the date portion of datetimes (we don't care about the times for
        # this chart)
        return [
            {"date": d["date"].date()} for d in await query_commit_dates(conn, repo_id)
        ]


@router.get("/chart-data/commits-per-author/{repo_id}")
async def get_commits_per_author(repo_id):
    async with db_connection() as conn:
        return await query_commits_per_author(conn, repo_id)


@router.get("/chart-data/line-counts-per-file/{repo_id}")
async def get_line_counts_per_file(repo_id):
    async with db_connection() as conn:
        return await query_line_counts_per_file(conn, repo_id)


@router.get("/chart-data/functional-line-counts-per-file/{repo_id}")
async def get_functional_line_counts_per_file(repo_id):
    async with db_connection() as conn:
        return await query_functional_line_counts_per_file(conn, repo_id)
