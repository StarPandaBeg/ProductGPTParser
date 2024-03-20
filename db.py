import pymongo
import psycopg
from config import config


def get_mongo_db():
    client = pymongo.MongoClient(config["mongo_connection_string"])
    db_name = config["mongo_database_name"]
    return client[db_name]


def get_postgres_db():
    return psycopg.connect(config["postgres_connection_string"])


def get_postgres_output_table():
    return config["postgres_output_table"]


def get_mongo_input_collection(db):
    collection_name = config["mongo_input_collection_name"]
    return db[collection_name]


def get_mongo_failed_collection(db):
    collection_name = config["mongo_failed_collection_name"]
    return db[collection_name]
