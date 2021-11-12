from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, globals
from ..dependencies import authenticate_user, create_access_token

router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post("/", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=globals.auth_config.access_token_expire_minutes)
    access_token = create_access_token(
        secret_key=globals.auth_config.secret_key,
        algorithm=globals.auth_config.algorithm,
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
