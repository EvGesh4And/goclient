import datetime, requests, json

from ..models.leader import Leader
from ..models.student import Student


def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

class RestStorage:
    def __init__(self, name):
        self.name = name
        self.group = None

    def select_type(self, d):
        if d["type"] == "leader":
            return Leader(io_handler=self.group.io_handler)
        else:
            return Student(io_handler=self.group.io_handler)

    def do_request(self, method, cmd="", data=""):
        try:
            url = f'http://127.0.0.1:5000/{self.name}/api/'
            header = None
            if (len(data)):
                header = {"Content-type": 'application/json'}
            res = method(url + cmd, headers=header, data=json.dumps(data, default=dateconverter))
            if res.status_code == 200:
                if res.content:
                    return json.loads(res.content)
                else:
                    return None
        except Exception as ex:
            print(ex)

    def load(self):
        pass

    def store(self):
        pass

    def clear(self):
        self.do_request(requests.delete)

    def get_item(self, id):
        if int(id) > 0:
            res = self.do_request(requests.get, str(id))
            if res:
                item = self.select_type(res)
                item.set_data(res)
            else:
                item = None
        return item

    def add(self, item):
        if int(item.id) <= 0:
            self.do_request(requests.post, data=item.get_data())
        else:
            self.do_request(requests.put, str(item.id), item.getData())

    def delete(self, id):
        self.do_request(requests.delete, str(id))

    def get_items(self):
        res = self.do_request(requests.get)
        for obj in res['ids']:
            yield self.get_item(obj['id'])
