from typing import Dict

from mongoengine import NotUniqueError, ValidationError

from app.models.users_model import Users


def sign_up(sign_up_info: Dict):
    u = Users(
        user_name=sign_up_info.get('user_name'),
        password=sign_up_info.get('password'),
        email=sign_up_info.get('email'),
        address=sign_up_info.get('address'),
        first_name=sign_up_info.get('first_name') if sign_up_info.get('first_name') else None,
        last_name=sign_up_info.get('last_name') if sign_up_info.get('last_name') else None,
        birthday=sign_up_info.get('birthday') if sign_up_info.get('birthday') else None,
        phone=sign_up_info.get('phone') if sign_up_info.get('phone') else None,
        gender=sign_up_info.get('gender') if sign_up_info.get('gender') else None,
        bio=sign_up_info.get('bio') if sign_up_info.get('bio') else None
    )
    try:
        u.save()
    except ValidationError:
        return {"message": "Bad input."}, 500
    except NotUniqueError as e:
        return {"message": "User already exists."}, 500
    else:
        return {}, 200
