from flask import Flask
from flask_restful import Api
from mongoengine import connect

from app.views.api_resources import api_resources

grulo_app = Flask(__name__)
grulo_api = Api(grulo_app)

connect(host="20.196.3.185:27018", db="grulo")

for resource in api_resources:
    grulo_api.add_resource(resource.get('name'), resource.get('path'))


if __name__ == "__main__":
    grulo_app.run(host='0.0.0.0', port=80, debug=True)
