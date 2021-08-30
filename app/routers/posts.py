from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends

from .. import exceptions
from .. import schemas
from ..database_crud import posts, models, groups
from ..dependencies import verify_logged_in, get_current_user
from ..globals import reverse_geocoder

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
def get_user_feed(start: int = 0, end: Optional[int] = None, user: models.User = Depends(get_current_user)) -> \
        List[schemas.Post]:
    try:
        posts_for_user = posts.get_user_feed(user)
        sorted_posts = sorted(posts_for_user, key=lambda x: x.last_update)[::-1]
        if end is None:
            return sorted_posts[start:]
        return sorted_posts[start:end]
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/explore/", response_model=List[schemas.Post])
def explore_posts_by_coor(start: int = 0, end: Optional[int] = None, lat: str = "32.08217107033524",
                          lon: str = "34.80586379620104") -> \
        List[schemas.Post]:
    try:
        places = reverse_geocoder.reverse_geocode(lat, lon)
        existing_groups = []
        for place in places:
            try:
                existing_groups.append(groups.get_group_by_name(place.name))
            except exceptions.NotFoundException:
                continue
        posts_for_user = [post for group in existing_groups for post in posts.get_posts_by_group_name(group.group_name)]
        sorted_posts = sorted(posts_for_user, key=lambda x: x.last_update)[::-1]
        if end is None:
            return sorted_posts[start:]
        return sorted_posts[start:end]
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
