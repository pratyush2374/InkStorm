from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    user_id: int


class ShowBlog(Blog):
    # author: ShowUser

    class Config:
        from_attributes = True
