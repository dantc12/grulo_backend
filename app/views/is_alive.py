from flask_restful import Resource


class IsAlive(Resource):
    def get(self):
        return "I'm alive bitch"
