from Database.database import Database


class DatabaseHandler:
    @staticmethod
    def insert(collection_name, document_id, document):
        return Database.insert(collection_name, document_id, document)

    @staticmethod
    def find(collection_name, document_id=None):
        return Database.find(collection_name, document_id)

    @staticmethod
    def update(collection_name, document_id, update):
        return Database.update(collection_name, document_id, update)

    @staticmethod
    def delete(collection_name, document_id=None):
        return Database.delete(collection_name, document_id)
