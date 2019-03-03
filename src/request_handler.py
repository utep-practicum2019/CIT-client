import requests

class RequestHandler:
    __domain = 'http://127.0.0.1:5000'
    __user_path = '/api/v2/resources/user'
    __group_path = '/api/v2/resources/group'
    __platform_path = '/api/v2/resources/platform'

    def get_user(username):
        data = {'username':username}
        r = requests.get(RequestHandler.__domain + RequestHandler.__user_path, json=data)
        return r.json()

    def get_group(group_id):
        data = {'group_id':group_id}
        r = requests.get(RequestHandler.__domain + RequestHandler.__group_path, json=data)
        return r.json()

    def get_platform(platform_id):
        data = {'platform_id':platform_id}
        r = requests.get(RequestHandler.__domain + RequestHandler.__platform_path, json=data)
        return r.json()
