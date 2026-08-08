from pydantic import BaseModel, ConfigDict
from typing import Optional

class AuthorSchema(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    bio: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
