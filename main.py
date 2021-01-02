from flask import Flask
from flask_restful import Resource, Api, reqparse

from app.views.api_resources import api_resources

grulo_app = Flask(__name__)
grulo_api = Api(grulo_app)

for v in api_resources:
    grulo_api.add_resource(v.get('name'), v.get('path'))


if __name__ == "__main__":
    grulo_app.run(host='0.0.0.0', port=443, debug=True)
