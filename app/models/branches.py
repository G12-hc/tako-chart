from pydantic import BaseModel

class Branch(BaseModel):
    id: int
    name: str
    repository_id: int
