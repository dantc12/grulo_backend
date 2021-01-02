from flask import Flask
from flask_restful import Resource, Api, reqparse

from app.views.api_configs import *
from app.views.is_alive import IsAlive
from app.views.login_resource import Login

grulo_app = Flask(__name__)
grulo_api = Api(grulo_app)

grulo_api.add_resource(IsAlive, IS_ALIVE_PATH)
grulo_api.add_resource(Login, LOGIN_PATH)


if __name__ == "__main__":
    grulo_app.run()
