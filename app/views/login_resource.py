from flask_restful import Resource, reqparse


class Login(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        return args, 200
