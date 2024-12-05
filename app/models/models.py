from pydantic import BaseModel
from datetime import datetime
from typing import List


class File(BaseModel):
    id: int
    is_directory: bool
    path: str
    name: str
    line_count: int
    functional_line_count: int
    symlink_target: str
    branch_id: int


class Commit(BaseModel):
    id: int
    sha: str
    date: datetime
    message: str
    author: str
    repository_id: str


class Repository(BaseModel):
    id: str
    external_id: int
    watchers: int
    forks_count: int
    name: str
    owner: str
    status: str
    linked_at: datetime
    modified_at: datetime
    contributors_url: str
    default_branch: str
    user_ids: List[int]
    archived_user_ids: List[int]
    licence_id: int
    workspace_id: str


class Branch(BaseModel):
    id: int
    name: str
    repository_id: str


class BranchCommit(BaseModel):
    branch_id: int
    commit_id: int


class Language(BaseModel):
    id: int
    name: str


class Licence(BaseModel):
    id: int
    key: str
    name: str
    spdx_id: str
    url: str
    node_id: str


class Workspace(BaseModel):
    id: str
    name: str
    owner_id: str