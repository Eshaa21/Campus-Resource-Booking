from pydantic import BaseModel


class ResourceCreate(BaseModel):
    name: str
    description: str | None = None
    location: str
    capacity: int | None = None
    category_id: int