from fastapi import FastAPI
from models import models
from database import engine
from routers.blog import blog_router
from routers.user import user_router
from routers.auth import auth_router


app = FastAPI()
models.Base.metadata.create_all(engine)


@app.get("/")
def root():
    return {"message": "Server up !"}

app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(user_router)