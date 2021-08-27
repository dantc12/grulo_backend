from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends

from .. import exceptions
from .. import schemas
from ..database_crud import posts, models
from ..dependencies import verify_logged_in, get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_logged_in)]
)


@router.post("/", response_model=schemas.Post)
def post_new_post(post: schemas.PostCreate, user: models.User = Depends(get_current_user)) -> schemas.Post:
    try:
        new_post = posts.create_post(post, user)
        return new_post
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


# TODO Continue here adding current user dependency when needed


@router.get("/{post_id}", response_model=schemas.Post)
def get_post_by_id(post_id: Optional[str] = None) -> schemas.Post:
    try:
        post = posts.get_post_by_id(post_id)
        return post
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/", response_model=List[schemas.Post])
def get_posts_by_identifier(group_name: Optional[str] = None,
                            username: Optional[str] = None) -> List[schemas.Post]:
    if group_name is None and username is None:
        raise HTTPException(400, "Must use an identifier for query.")
    try:
        if group_name is not None:
            found_posts = posts.get_posts_by_group_name(group_name)
        else:  # username is not None:
            found_posts = posts.get_posts_by_user(username)
        return found_posts
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/comment/{post_id}", response_model=schemas.Post)
def add_comment_to_post(post_id: str, comment: schemas.CommentCreate,
                        user: models.User = Depends(get_current_user)) -> schemas.Post:
    try:
        post = posts.add_comment_to_post(post_id, comment, user)
        return post
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/feed/", response_model=List[schemas.Post])
def get_user_feed(range: schemas.RangeSearch, user: models.User = Depends(get_current_user)) -> \
        List[schemas.Post]:
    try:
        posts_for_user = posts.get_user_feed(user)
        sorted_posts = sorted(posts_for_user, key=lambda x: x.last_update)[::-1]
        if range.max is not None:
            return sorted_posts[range.min:range.max]
        else:
            return sorted_posts[range.min:]
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
