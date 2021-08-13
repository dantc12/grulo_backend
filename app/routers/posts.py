from typing import Optional, List

from fastapi import APIRouter, HTTPException

from .. import exceptions
from .. import schemas
from ..database_crud import posts

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post("/")
def post_new_post(post: schemas.PostCreate) -> schemas.Post:
    try:
        new_post = posts.create_post(post)
        return schemas.Post(**new_post.to_dict())
    except exceptions.UserNotFound as e:
        raise HTTPException(404, str(e))
    except exceptions.GroupNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/{post_id}")
def get_post_by_id(post_id: Optional[str] = None) -> schemas.Post:
    try:
        post = posts.get_post_by_id(post_id)
        return schemas.Post(**post.to_dict())
    except exceptions.PostNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/")
def get_posts(group_name: Optional[str] = None,
              group_id: Optional[str] = None,
              username: Optional[str] = None) -> List[schemas.Post]:
    if group_name is None and group_id is None and username is None:
        raise HTTPException(400, "Must use an identifier for query.")
    try:
        if group_name is not None:
            found_posts = posts.get_posts_by_group_name(group_name)
        elif group_id is not None:
            found_posts = posts.get_posts_by_group_id(group_id)
        else:  # username is not None:
            found_posts = posts.get_posts_by_user(username)
        return [schemas.Post(**post.to_dict()) for post in found_posts]
    except exceptions.GroupNotFound as e:
        raise HTTPException(404, str(e))
    except exceptions.UserNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/comment/{post_id}")
def add_comment_to_post(post_id: str, comment: schemas.CommentCreate) -> schemas.Post:
    try:
        post = posts.add_comment_to_post(post_id, comment)
        return schemas.Post(**post.to_dict())
    except exceptions.PostNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/for_user/{username}")
def get_all_posts_for_user(username: str, limit: Optional[int] = None) -> List[schemas.Post]:
    try:
        posts_for_user = posts.get_posts_for_user(username, limit)
        return [schemas.Post(**post.to_dict()) for post in posts_for_user]
    except exceptions.UserNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
