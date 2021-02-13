from flask import Flask
from flask_restful import Api
from mongoengine import connect

from app.api_resources import api_resources
from config import *

grulo_app = Flask(__name__)
grulo_api = Api(grulo_app)

connect(host=MONGO_HOST, port=MONGO_PORT, db=DB_NAME)

for resource in api_resources:
    grulo_api.add_resource(resource.get('name'), resource.get('path'))


if __name__ == "__main__":
    grulo_app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
