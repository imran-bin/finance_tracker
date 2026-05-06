from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    type: str
    user_id: int

class CategoryOut(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True