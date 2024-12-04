from pydantic import BaseModel

class File(BaseModel):
    id: int
    name: str
    path: str
    line_count: int
    functional_line_count: int
    branch_id: int
