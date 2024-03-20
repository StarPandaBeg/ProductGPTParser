from abc import abstractmethod, ABC


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
        self._db.execute(self._query, data)


class MongoHandler(ResponseHandler):

    def __init__(self, collection):
        super().__init__()
        self._collection = collection

    def handle(self, item, data):
        if (isinstance(data, list)):
            self._collection.insert_many(data)
        else:
            self._collection.insert_one(data)
