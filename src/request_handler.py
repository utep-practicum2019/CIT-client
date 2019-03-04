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
        data = {'platform_name':platform_id}
        r = requests.get(RequestHandler.__domain + RequestHandler.__platform_path, json=data)
        return r.json()

    def list_plarforms(user_id):
        # TODO: test/fix this method, should list all platforms for a group
        group = RequestHandler.get_group(user_id)
        tmp = {}
        for p in group['platforms']:
            plat = RequestHandler.get_platform(p)
            tmp[p] = p['subplatforms']
        return tmp
