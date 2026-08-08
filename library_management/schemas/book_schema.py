from pydantic import BaseModel, ConfigDict
from typing import Optional
from schemas.author_schema import AuthorSchema

class BookCreateSchema(BaseModel):
    title: str
    price: float
    author_id: int

class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    author_id: Optional[int] = None

class BookResponseSchema(BookCreateSchema):
    id: int
    author: Optional[AuthorSchema] = None
    
    model_config = ConfigDict(from_attributes=True)
