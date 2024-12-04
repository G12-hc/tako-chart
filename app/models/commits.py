from pydantic import BaseModel

class Commit(BaseModel):
    id: int
    sha: str
    date: str
    message: str
    author: str
    repository_id: int


