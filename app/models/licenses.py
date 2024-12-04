from pydantic import BaseModel

class License(BaseModel):
    id: int
    name: str
    spdx_id: str
    url: str
    node_id: str
