from fastapi import APIRouter
from app.db import get_db_connection
from app.db.queries import (
    query_languages,
    query_licenses,
    query_repo,
    query_commit,
    query_branches,
    query_files,
    query_repos,
    query_workspaces,
)

router = APIRouter(prefix="/repos")

@router.get("/")
def get_all_repos():
    conn = get_db_connection()
    repos = query_repos(conn)
    return {"repos": repos}


@router.get("/{repo_id}")
def get_all_repo_data(repo_id):
    conn = get_db_connection()
    languages = query_languages(conn, repo_id)
    licenses = query_licenses(conn, repo_id)
    commits = query_commit(conn, repo_id)
    branches = query_branches(conn, repo_id)
    files = query_files(conn, 100)
    repo = query_repo(conn, repo_id)
    workspace = query_workspaces(conn, repo_id)
    return {
        "languages": languages,
        "licenses": licenses,
        "repository": repo,
        "commits": commits,
        "branches": branches,
        "files": files,
        "workspace": workspace,
    }
