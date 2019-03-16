"""
    TODO: Implementation and integration for platforms
    TODO: Testing with users
    TODO: Testing with groups
    Platforms shouldn't change it much because it's pretty generic.
"""

from pymongo import MongoClient


class Database:
    __client = MongoClient('localhost', 27017)
    __db = __client['cit']
    __users = __db['users']
    __groups = __db['groups']
    # __platforms = __db['platforms']
    collection = {
        'users': __users,
        'groups': __groups,
        # 'platforms': __platforms
    }

    @staticmethod
    def insert(collection_name, document_id, document):
        try:
            if Database.find(collection_name, document_id):
                # already exists
                return False
            Database.collection[collection_name].insert_one(document)
            return True
        except KeyError:
            # collection does not exist
            return False

    @staticmethod
    def find(collection_name, document_id):
        if collection_name == 'users':
            doc_id = {'username': document_id}
        elif collection_name == 'groups':
            doc_id = {'group_id': document_id}
        elif collection_name == 'platforms':
            doc_id = {'platforms': document_id}
        else:
            doc_id = None

        try:
            if document_id is None:
                # get all users
                cursor = Database.collection[collection_name].find()
                users = []
                while True:
                    try:
                        user = cursor.next()
                        del user['_id']
                        users.append(user)
                    except StopIteration:
                        return users
            # get a single user
            doc = Database.collection[collection_name].find_one(doc_id)
            if doc is not None:
                del doc['_id']
            return doc
        except KeyError:
            return False

    @staticmethod
    def update(collection_name, document_id, document):
        if collection_name == 'users':
            doc_id = {'username': document_id}
        elif collection_name == 'groups':
            doc_id = {'group_id': document_id}
        elif collection_name == 'platforms':
            doc_id = {'platforms': document_id}
        else:
            doc_id = None

        try:
            setter = {'$set': document}
            old_doc = Database.collection[collection_name].find_one_and_update(doc_id, setter)
            if old_doc is not None:
                return True
            return False
        except KeyError:
            return False

    @staticmethod
    def delete(collection_name, document_id=None):
        if collection_name == 'users':
            doc_id = {'username': document_id}
        elif collection_name == 'groups':
            doc_id = {'group_id': document_id}
        elif collection_name == 'platforms':
            doc_id = {'platforms': document_id}
        else:
            doc_id = None

        if None:
            Database.collection[collection_name].drop()
        else:
            try:
                del_doc = Database.collection[collection_name].find_one_and_delete(doc_id)
                if del_doc is not None:
                    return True
                return False
            except KeyError:
                return False
