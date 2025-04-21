from typing import List
from pydantic import BaseModel
from schemas.blog_schema import ShowBlog

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[ShowBlog]

    class Config:
        from_attributes = True
        
