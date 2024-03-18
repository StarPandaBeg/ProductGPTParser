import pymongo
from config import config


def get_db():
    client = pymongo.MongoClient(config["connection_string"])
    db_name = config["database_name"]
    return client[db_name]


def get_input_collection(db):
    collection_name = config["input_collection_name"]
    return db[collection_name]


def get_output_collection(db):
    collection_name = config["output_collection_name"]
    return db[collection_name]


def get_failed_collection(db):
    collection_name = config["failed_collection_name"]
    return db[collection_name]
