from os import environ as env

config = {
    "connection_string": env.get("PGPT_CONNECTION_STRING", "mongodb://localhost:27017"),
    "database_name": env.get("PGPT_DB_NAME", "posts"),
    "failed_collection_name": env.get("PGPT_FAILED_COLLECTION_NAME", "posts_failed"),
    "input_collection_name": env.get("PGPT_INPUT_COLLECTION_NAME", "posts"),
    "output_collection_name": env.get("PGPT_OUTPUT_COLLECTION_NAME", "posts_parsed"),
    "per_request_delay": int(env.get("PGPT_REQUEST_DELAY", 2))
}
