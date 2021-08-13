from fastapi import APIRouter, HTTPException

from .. import schemas, exceptions
from ..database_crud import users

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/")
async def sign_up(user: schemas.UserCreate) -> schemas.User:
    try:
        db_user = users.create_user(user)
        return schemas.User(**db_user.to_dict())
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/{username}")
async def get_user(username: str) -> schemas.User:
    try:
        db_user = users.get_user_by_name(username)
        return schemas.User(**db_user.to_dict())
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
