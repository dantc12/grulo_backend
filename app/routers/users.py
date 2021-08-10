from fastapi import APIRouter, Depends, HTTPException

from .. import database
from .. import schemas, exceptions
from ..database_crud import users

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(database.connect_to_db)]  # TODO add the security part
)


# TODO add handling of mongo db errors such as non-unique, already exist, invalid format (email, date)

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
    except exceptions.UserNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
