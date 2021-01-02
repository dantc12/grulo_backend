from flask_restful import Resource


class SignUp(Resource):
    def get(self):
        return "This is the sign-up API"
