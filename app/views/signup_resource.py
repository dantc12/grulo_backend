from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError, ValidationError

from app.models import Users


class SignUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('address', required=True)
        parser.add_argument('birthday')
        parser.add_argument('phone')
        parser.add_argument('gender')
        parser.add_argument('bio')
        args = parser.parse_args()  # parse arguments to dictionary

        u = Users(
            username=args.get('username'),
            password=args.get('password'),
            email=args.get('email'),
            address=args.get('address'),
            birthday=args.get('birthday') if args.get('birthday') else None,
            phone=args.get('phone') if args.get('phone') else None,
            gender=args.get('gender') if args.get('gender') else None,
            bio=args.get('bio') if args.get('bio') else None
        )
        try:
            u.save()
        except ValidationError:
            return {"message": "Bad input."}, 500
        except NotUniqueError as e:
            print(e)
            return {"message": "User already exists."}, 500
        else:
            response = {"message": "User created successfully."}
            response.update(u.json())
            return response, 200
