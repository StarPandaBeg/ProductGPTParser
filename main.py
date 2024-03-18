from db import *
from gptparser import parse
from bson.objectid import ObjectId


def process(db):
    posts = get_input_collection(db)
    output = get_output_collection(db)
    failed = get_failed_collection(db)

    i = 1
    for item in posts.find():
        item_id = item['_id']
        item.pop('_id')

        print(f"Parsing №{i} ({item_id}) - ", end='')
        status, data = parse(item)
        target_collection = output if status else failed

        if (isinstance(data, list)):
            target_collection.insert_many(data)
        else:
            target_collection.insert_one(data)

        print("OK" if status else "FAIL")
        i += 1


db = get_db()
process(db)
