from abc import abstractmethod, ABC
from json import dumps


class ResponseHandler(ABC):

    @abstractmethod
    def handle(self, item, data):
        pass


class PostgresHandler(ResponseHandler):
    def __init__(self, db, table_name):
        super().__init__()
        self._db = db
        self._table = table_name
        self._query = f"INSERT INTO {self._table} (name, description, price, contact, post_date, post_attachments, post_id, post_owner_id) VALUES (%(name)s,%(description)s, %(price)s, %(contact)s, %(post_date)s, %(post_attachments)s, %(post_id)s, %(post_owner_id)s)"
        self._create_table()

    def handle(self, item, data):
        if (isinstance(data, list)):
            for row in data:
                self._insert_row(row)
        else:
            self._insert_row(data)
        self._db.commit()

    def _insert_row(self, data):
        if "description" not in data:
            data["description"] = ""
        if "contact" not in data:
            data["contact"] = ""
        if "post_attachments" in data:
            data["post_attachments"] = dumps(data["post_attachments"])
        self._db.execute(self._query, data)

    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self._table} (
            "id" SERIAL PRIMARY KEY,
            "name" varchar(255) NOT NULL,
            "description" text,
            "price" numeric(10,2) NOT NULL,
            "contact" varchar(255),
            "post_date" timestamp(0),
            "post_attachments" jsonb,
            "post_id" int4,
            "post_owner_id" int4
        );
        """
        try:
            self._db.execute(query)
            self._db.commit()
        except:
            self._db.rollback()
            raise


class MongoHandler(ResponseHandler):

    def __init__(self, collection):
        super().__init__()
        self._collection = collection

    def handle(self, item, data):
        if (isinstance(data, list)):
            self._collection.insert_many(data)
        else:
            self._collection.insert_one(data)
