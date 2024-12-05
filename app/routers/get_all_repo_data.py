from fastapi import APIRouter
from app.db import get_db_connection
from app.db.queries import query_languages, query_licenses, query_repositories, query_commit, query_branches, \
    query_files, query_repo

router = APIRouter(prefix="/repo_data")
@router.get("/{repo_id}")
def get_all_repo_data(repo_id):
    with get_db_connection() as conn:
        languages = query_languages(conn, repo_id)
        licenses = query_licenses(conn, repo_id)
        repository = query_repositories(conn, repo_id)
        commits = query_commit(conn, repo_id)
        branches = query_branches(conn, repo_id)
        files = query_files(conn, repo_id)
        repo = query_repo(conn)
        return {"languages": languages, "licenses": licenses, "repository": repository, "commits": commits, "branches": branches, "files": files, "Return all repo": repo}



@router.get("/{repo_id}")
def get_commits(repo_id):
    with get_db_connection() as conn:
        return query_commit(conn, repo_id)
