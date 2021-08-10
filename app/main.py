from fastapi import FastAPI

from .routers import users, posts, groups

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(groups.router)
