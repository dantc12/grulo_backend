from mongoengine import connect
from . import dependencies


# TODO this should be done once
def connect_to_db():
    connect(**dependencies.mongo_config)
