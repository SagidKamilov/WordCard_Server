from pydantic import BaseModel


class CategoryCreate(BaseModel):
    category_name: str


class CategoryUpdate(BaseModel):
    category_name: str


class CategoryResponse(BaseModel):
    id: int
    category_name: str
    owner_id: int
