from fastapi import APIRouter, HTTPException, Depends

from .. import schemas, exceptions
from ..database_crud import users
from ..dependencies import get_current_user, get_password_hash, verify_logged_in

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=schemas.User)
async def sign_up(user: schemas.UserCreate) -> schemas.User:
    try:
        user.password = get_password_hash(user.password)
        db_user = users.create_user(user)
        return db_user
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.get("/{username}", response_model=schemas.User, responses={404: {"description": "Not found"}},
            dependencies=[Depends(verify_logged_in)])
async def get_user(username: str) -> schemas.User:
    try:
        db_user = users.get_user_by_name(username)
        return schemas.User(**db_user.to_dict())
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
