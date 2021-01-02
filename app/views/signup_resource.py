from flask_restful import Resource, reqparse
from app.models import Users
import json


class SignUp(Resource):
    def get(self):
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
            address=args.get('address')
            # birthday=args.get('birthday') if args.get('birthday') else "",
            # phone=args.get('phone') if args.get('phone') else "",
            # gender=args.get('gender') if args.get('gender') else "",
            # bio=args.get('bio') if args.get('bio') else ""
        )
        u.save()
        print(str(Users.objects.get(username='dan')))

        return u.json(), 200
