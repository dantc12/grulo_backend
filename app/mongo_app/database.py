from mongoengine import connect


def connect_to_db(mongo_host: str, mongo_port: int, db_name: str):
    connect(host=mongo_host, port=mongo_port, db=db_name)