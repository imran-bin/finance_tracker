from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    type: str
    user_id: int

class CategoryUpdate(BaseModel):
    name: str
    type: str
    user_id: int
