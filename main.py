from db import *
from config import config
from gptparser import parse
from response_handler import PostgresHandler, MongoHandler


def process():
    mongo = get_mongo_db()
    postgres = get_postgres_db()

    posts = get_mongo_input_collection(mongo)
    failed = get_mongo_failed_collection(mongo)

    success_handler = PostgresHandler(postgres, get_postgres_output_table())
    fail_handler = MongoHandler(failed)

    i = 1
    for item in posts.find():
        item_id = item['_id']
        item.pop('_id')

        print(f"Parsing №{i} ({item_id}) - ", end='')
        status, data = parse(item)
        handler = success_handler if status else fail_handler

        try:
            handler.handle(item, data)
        except:
            fail_handler.handle(item, data)

        if (config["delete_processed"]):
            posts.delete_one({"_id": item_id})

        print("OK" if status else "FAIL")
        i += 1
    postgres.close()


process()
