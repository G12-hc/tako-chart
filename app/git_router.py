from fastapi import APIRouter, HTTPException
from app.db.fetch_git_api import (get_repository_details,
                                  get_commit_history,
                                  get_contributors)
router = APIRouter()

@router.get("/github/repository/{owner}/{repo}")
async def repository_details(owner: str, repo: str):
    # Fetch details about a specific GitHub repository.
    try:
        repo_details = await get_repository_details(owner, repo)
        return repo_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/github/repository/{owner}/{repo}/commits")
async def commit_history(owner: str, repo: str):
    # Fetch the commit history of a specific GitHub repository.
    try:
        commits = await get_commit_history(owner, repo)
        return commits
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/github/repository/{owner}/{repo}/contributors")
async def contributors(owner: str, repo: str):
    # Fetch the repo_contributors of a specific GitHub repository.
    try:
        repo_contributors = await get_contributors(owner, repo)
        return repo_contributors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
