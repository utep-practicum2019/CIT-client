# import sqlite3
from flask import Flask, request, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

import inputValidator as inputValidator
from CITAPI_Schema import *

ma = Marshmallow()

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@auth.get_password
def get_password(username):
    if username == 'root':
        return 'toor'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# class BookAPI(Resource):
#
#     def get(self):
#
#         query_parameters = request.args
#
#         id = query_parameters.get('id')
#         published = query_parameters.get('published')
#         author = query_parameters.get('author')
#
#         query = "SELECT * FROM books WHERE"
#
#         to_filter = []
#
#         if id:
#             query += ' id=? AND'
#             to_filter.append(id)
#         if published:
#             query += ' published=? AND'
#             to_filter.append(published)
#         if author:
#             query += ' author=? AND'
#             to_filter.append(author)
#
#         # if not (id or published or author):
#         #     return page_not_found(404)
#
#         query = query[:-4] + ';'
#         conn = sqlite3.connect('books.db')
#         conn.row_factory = dict_factory
#         cur = conn.cursor()
#         results = cur.execute(query, to_filter).fetchall()
#         return results, 404
#
#
# class BookListAPI(Resource):
#     def get(self):
#         conn = sqlite3.connect('books.db')
#         conn.row_factory = dict_factory
#         cur = conn.cursor()
#         all_books = cur.execute('SELECT * FROM books;').fetchall()
#         return all_books


class LoginAPI(Resource):
    decorators = [auth.login_required]

    def post(self):

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = login_schema.load(json_data)

        if errors:
            return errors, 422
        if not inputValidator.is_valid_ipv4_address(data['ip']):
            return {'message': 'Not a valid IP address'}, 400
        return "Authenticated User, Assigned " + data['ip'] + " Redirect To: "


class VMConfigAPI(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = vm_config_schema.load(json_data)

        if errors:
            return errors, 422

        command = ""
        if 'vmName' in data:
            command += "vmname " + data['vmName'] + " "
        if 'src_ip' in data:
            if inputValidator.is_valid_ipv4_address(data['src_ip']):
                command += "src_ip " + data['src_ip'] + " "
            else:
                return {'message': 'Not a valid IP address'}, 400
        if 'src_prt' in data:
            command += "src_prt" + data['src_prt'] + " "
        if 'dst_ip' in data:
            if inputValidator.is_valid_ipv4_address(data['src_ip']):
                command += "dst_ip " + data['dst_ip'] + " "
            else:
                return {'message': 'Not a valid IP address'}, 400
        if 'dst_prt' in data:
            command += "dst_prt " + data['dst_prt'] + " "
        if 'adpt_number' in data:
            command += "adpt_number " + data['adpt_number'] + " "
        results = ({'config': command})
        return results


class VMStatusAPI(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = vm_status_schema.load(json_data)

        if errors:
            return errors, 422

        command = ""
        if 'vmName' in data:
            command += "vmname " + data['vmName'] + " "
        if 'mgrStatus' in data:
            command += "mgrstatus " + data['mgrStatus']
        results = ({'status': command})
        return results


class VMStartAPI(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = vm_start_schema.load(json_data)

        if errors:
            return errors, 422

        command = ""
        if 'vmName' in data:
            command += "vmname " + data['vmName']
        results = ({'start': command})
        return results


class VMSuspendAPI(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = vm_suspend_schema.load(json_data)

        if errors:
            return errors, 422

        command = ""
        if 'vmName' in data:
            command += "vmname " + data['vmName']
        results = ({'suspend': command})
        return results


class PlatformAPI(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = platform_schema.load(json_data)

        if errors:
            return errors, 422

        results = {
            'port': '8080',
            'links': 'placeholder',
            'status_code': 2,
            'comm_tunnel': 1,
            'server_subsys_name': 'platform'
        }

        return results


# api.add_resource(BookAPI, '/api/v2/resources/books')
# api.add_resource(BookListAPI, '/api/v2/resources/books/all')

api.add_resource(PlatformAPI, '/api/v2/resources/platform')
api.add_resource(VMConfigAPI, '/api/v2/resources/vm/manage/config')
api.add_resource(VMStatusAPI, '/api/v2/resources/vm/manage/status')
api.add_resource(VMStartAPI, '/api/v2/resources/vm/manage/start')
api.add_resource(VMSuspendAPI, '/api/v2/resources/vm/manage/suspend')
api.add_resource(LoginAPI, '/api/v2/resources/login')

if __name__ == '__main__':
    app.run()
