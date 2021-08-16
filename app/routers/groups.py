from typing import List

from fastapi import APIRouter, HTTPException, Depends

from .. import schemas, exceptions
from ..database_crud import groups, models
from ..dependencies import verify_logged_in, get_current_user
from ..globals import reverse_geocoder

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    dependencies=[Depends(verify_logged_in)]
)


@router.get("/get_by_coor", response_model=List[schemas.QueryGroup])
async def explore_groups_by_coor(lat: str = "32.08217107033524", lon: str = "34.80586379620104") -> \
        List[schemas.QueryGroup]:
    try:
        places = reverse_geocoder.reverse_geocode(lat, lon)
        return [schemas.QueryGroup(group_name=place.name, group_type=place.type) for place in places]
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/", response_model=List[schemas.Group])
async def get_all_groups() -> List[schemas.Group]:
    try:
        result_groups = groups.get_all_groups()
        return result_groups
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/", response_model=schemas.Group)
async def get_group_by_name(group_name: str) -> schemas.Group:
    try:
        group = groups.get_group_by_name(group_name)
        return group
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/", response_model=schemas.Group)
async def join_group(query_group: schemas.QueryGroup, user: models.User = Depends(get_current_user)) -> schemas.Group:
    try:
        group = groups.add_user_to_group(query_group, user)
        return group
    except exceptions.NotFoundException as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
