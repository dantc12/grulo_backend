from typing import List

from fastapi import APIRouter, HTTPException

from .. import schemas, exceptions
from ..database_crud import groups
from ..globals import reverse_geocoder

router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)


# TODO add handling of mongo db errors such as non-unique, already exist, invalid format (email, date)

@router.get("/get_by_coor")
async def explore_groups_by_coor(lat: str, lon: str) -> List[schemas.QueryGroup]:
    try:
        places = reverse_geocoder.reverse_geocode(lat, lon)
        return [schemas.QueryGroup(group_name=place.name, group_type=place.type) for place in places]
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/")
async def get_all_groups() -> List[schemas.Group]:
    try:
        result_groups = groups.get_all_groups()
        return [schemas.Group(**result_group.to_dict()) for result_group in result_groups]
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/{group_id}")
async def get_group_by_id(group_id: str) -> schemas.Group:
    try:
        group = groups.get_group_by_id(group_id)
        return schemas.Group(**group.to_dict())
    except exceptions.GroupNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/")
async def add_user_to_group(query_group: schemas.QueryGroup, username: str) -> schemas.Group:
    try:
        group = groups.add_user_to_group(query_group, username)
        return schemas.Group(**group.to_dict())
    except exceptions.GroupNotFound as e:
        raise HTTPException(404, str(e))
    except exceptions.UserNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
