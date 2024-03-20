from os import environ as env

config = {
    "mongo_connection_string": env.get("PGPT_MONGO_CONNECTION_STRING", "mongodb://localhost:27017"),
    "mongo_database_name": env.get("PGPT_MONGO_DB", "posts"),
    "mongo_failed_collection_name": env.get("PGPT_MONGO_FAILED_COLLECTION", "posts_failed"),
    "mongo_input_collection_name": env.get("PGPT_MONGO_INPUT_COLLECTION", "posts"),

    "postgres_connection_string": env.get("PGPT_MONGO_CONNECTION_STRING", "postgresql://postgres@localhost/parser"),
    "postgres_output_table": env.get("PGPT_POSTGRES_OUTPUT_TABLE", "output"),

    "per_request_delay": int(env.get("PGPT_REQUEST_DELAY", 2)),
}
