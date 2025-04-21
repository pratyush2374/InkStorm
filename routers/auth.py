import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from hashing import verify
from models.models import UserModel
from schemas.auth_schema import Login
from tokens import create_access_token


auth_router = APIRouter(tags=["Auth routes"], prefix="/auth")


@auth_router.post("/login")
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == req.username).first()
    if not user:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_404_NOT_FOUND
        )
    if not verify(user.password, req.password):
        raise HTTPException(
            detail="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED
        )

    ACCESS_TOKEN_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY"))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=ACCESS_TOKEN_EXPIRY
    )

    return {"access_token": access_token, "token_type": "bearer"}
