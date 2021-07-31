from mongoengine import connect

from config import *
from flask_cors import CORS
import connexion

grulo_app = connexion.App(__name__)
CORS(grulo_app.app)
grulo_app.add_api('swagger.yml')



if __name__ == "__main__":
    grulo_app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
