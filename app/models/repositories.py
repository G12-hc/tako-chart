from fastapi import APIRouter, HTTPException
from app.routers.repositories import get_repository_stats


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