from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from database import get_db
from models.models import BlogModel
from oauth import get_current_user
from schemas.blog_schema import ShowBlog, Blog
from schemas.user_schema import User

blog_router = APIRouter(
    tags=["Blog routes"]
    # prefix="/blog" ---> to add blog after each route
)


@blog_router.get("/blogs", response_model=List[ShowBlog])
def get_blogs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)  ):
    blogs = db.query(BlogModel).all()
    return blogs


@blog_router.post("/post-blog", status_code=status.HTTP_201_CREATED)
def post_blog(blog_req: Blog, db: Session = Depends(get_db)):
    new_blog = BlogModel(
        title=blog_req.title, body=blog_req.body, user_id=blog_req.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@blog_router.get("/blogs", response_model=List[ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


@blog_router.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=ShowBlog)
def get_blogs_by_id(id: int, db: Session = Depends(get_db)):
    blog_by_id = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog id {id} not found"
        )
    return blog_by_id


@blog_router.delete("/delete-blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    db.query(BlogModel).filter(BlogModel.id == id).delete(synchronize_session=False)
    db.commit()


@blog_router.put("/update-blog/{id}")
def update_blog(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    blog.update(
        {"title": request.title, "body": request.body}, synchronize_session=False
    )
    db.commit()
    return blog.first()
