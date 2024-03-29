from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users, posts, groups, login

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=False,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(login.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(groups.router)
