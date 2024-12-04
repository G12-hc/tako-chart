from fastapi import APIRouter, HTTPException
from app.services.repositories import get_repository_stats

router = APIRouter()

@router.get("/repositories/{repo_id}/stats")
def fetch_repository_stats(repo_id: int):
    """
    Endpoint to fetch repository statistics.
    """
    stats = get_repository_stats(repo_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Repository not found")
    return stats


class RepositoryStats:
    def __init__(self, commit_count: int, branch_count: int, file_count: int):
        self.commit_count = commit_count
        self.branch_count = branch_count
        self.file_count = file_count

    def to_dict(self):
        return {
            "commit_count": self.commit_count,
            "branch_count": self.branch_count,
            "file_count": self.file_count,
        }