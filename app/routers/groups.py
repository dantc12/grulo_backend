from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends

from .. import schemas, exceptions
from ..database_crud import groups, models, posts
from ..dependencies import verify_logged_in, get_current_user
from ..globals import reverse_geocoder

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    dependencies=[Depends(verify_logged_in)]
)


@router.get("/explore", response_model=List[schemas.QueryGroup])
async def explore_groups_by_coor(lat: str = "32.08217107033524", lon: str = "34.80586379620104") -> \
        List[schemas.QueryGroup]:
    try:
        places = reverse_geocoder.reverse_geocode(lat, lon)
        return [schemas.QueryGroup(group_name=place.name, group_type=place.type) for place in places]
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/all", response_model=List[schemas.Group])
async def get_all_groups() -> List[schemas.Group]:
    try:
        result_groups = groups.get_all_groups()
        return result_groups
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/", response_model=schemas.Group)
async def get_group(id: Optional[str] = None, group_name: Optional[str] = None) -> schemas.Group:
    try:
        if id is not None:
            return groups.get_group_by_id(id)
        if group_name is not None:
            return groups.get_group_by_name(group_name)
        raise exceptions.BadInput()
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except exceptions.BadInput as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/search/", response_model=List[schemas.Group])
async def search_groups(group_name: str) -> List[schemas.Group]:
    possible_matches = groups.search_groups_containing(group_name)
    return possible_matches


@router.post("/", response_model=schemas.Group)
async def join_group(query_group: schemas.QueryGroup, user: models.User = Depends(get_current_user)) -> schemas.Group:
    try:
        group = groups.add_user_to_group(query_group, user)
        return group
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/{id}/posts", response_model=List[schemas.Post], responses={404: {"description": "Not found"}},
            dependencies=[Depends(verify_logged_in)])
async def get_posts_of_group(id: str):
    try:
        group = groups.get_group_by_id(id)
        return posts.get_posts_of_group(str(group.id))
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
