from mongoengine import connect

from config import *
import connexion

grulo_app = connexion.App(__name__)
grulo_app.add_api('swagger.yml')

connect(host=MONGO_HOST, port=MONGO_PORT, db=DB_NAME)

if __name__ == "__main__":
    grulo_app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
