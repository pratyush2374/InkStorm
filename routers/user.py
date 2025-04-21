from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from hashing import hash_string
from models.models import UserModel
from schemas.user_schema import ShowUser, User

user_router = APIRouter(tags=["User routes"])


@user_router.post("/register-user", response_model=ShowUser)
def register_user(request: User, db: Session = Depends(get_db)):
    new_user = UserModel(
        name=request.name, email=request.email, password=hash_string(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get("/user/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
