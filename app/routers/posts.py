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
        return posts.create_post(post, user)
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/", response_model=schemas.Post)
def get_post_by_id(id: str) -> schemas.Post:
    try:
        return posts.get_post_by_id(id)
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/{id}/comment", response_model=schemas.Post)
def add_comment_to_post(id: str, comment: schemas.CommentCreate,
                        user: models.User = Depends(get_current_user)) -> schemas.Post:
    try:
        return posts.add_comment_to_post(id, comment, user)
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/{id}/comment_like", response_model=schemas.Post)
def like_comment_of_post(id: str, comment_index: int,
                         user: models.User = Depends(get_current_user)) -> schemas.Post:
    try:
        return posts.like_comment_of_post(id, comment_index, user)
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/{id}/comment_unlike", response_model=schemas.Post)
def unlike_comment_of_post(id: str, comment_index: int,
                           user: models.User = Depends(get_current_user)) -> schemas.Post:
    try:
        return posts.unlike_comment_of_post(id, comment_index, user)
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/{id}/like", response_model=schemas.Post)
def like_post(id: str, user: models.User = Depends(get_current_user)) -> schemas.Post:
    try:
        return posts.like_post(id, user)
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/{id}/unlike", response_model=schemas.Post)
def unlike_post(id: str, user: models.User = Depends(get_current_user)) -> schemas.Post:
    try:
        return posts.unlike_post(id, user)
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
        posts_for_user = [post for group in existing_groups for post in posts.get_posts_of_group(str(group.id))]
        sorted_posts = sorted(posts_for_user, key=lambda x: x.last_update)[::-1]
        if end is None:
            return sorted_posts[start:]
        return sorted_posts[start:end]
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
