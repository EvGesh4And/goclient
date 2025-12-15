import datetime
import requests
import json
from typing import Dict, Optional

from app.akm2501.st18.models import Item, Employee, Student


def date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class RestStorage:
    def __init__(self, base_url: str = "http://localhost:5000", student_title: str = "[2501-18] Сунагатова"):
        self.__base_url = base_url
        self.__student_title = student_title
        self.__st_prefix = self.__get_st_prefix()
        self.__api_url = f"{base_url}{self.__st_prefix}/api"

    def __get_st_prefix(self) -> str:
        try:
            response = requests.get(f"{self.__base_url}/api/")
            response.raise_for_status()
            data = response.json()

            for st_number, title in data.get('sts', []):
                if title == self.__student_title:
                    return f"/st{st_number}"

            return "/st1"
        except requests.RequestException:
            return "/st1"

    def __do_request(self, method, cmd: str = "", data=None):
        try:
            url = f'{self.__api_url}/'
            headers = {'Content-Type': 'application/json'}
            res = method(url + cmd, data=json.dumps(data, default=date_converter), headers=headers)
            if res.status_code in (200, 201):
                if res.content:
                    return json.loads(res.content)
                else:
                    return None
        except Exception as ex:
            print(ex)
            return None

    def load(self):
        items = self.get_items()
        max_id = max(items.keys()) if items else 0
        return max_id, items

    def store(self, max_id: int, items: Dict[int, Item]):
        pass

    def get_items(self) -> Dict[int, Item]:
        res = self.__do_request(requests.get)
        items = {}
        if res and 'items' in res:
            for item_data in res['items']:
                item_type = item_data.get('type')
                if item_type == 'student':
                    item = Student()
                elif item_type == 'employee':
                    item = Employee()
                else:
                    continue
                item.set_data(item_data)
                items[item.id] = item
        return items

    def get(self, id: int) -> Optional[Item]:
        res = self.__do_request(requests.get, str(id))
        if res:
            item_type = res.get('type')
            if item_type == 'student':
                item = Student()
            elif item_type == 'employee':
                item = Employee()
            else:
                return None
            item.set_data(res)
            return item
        return None

    def add(self, item: Item) -> int:
        data = item.get_data()
        item_type = self.__get_item_type_name(item)
        data['type'] = item_type

        res = self.__do_request(requests.post, data=data)
        if res and 'id' in res:
            return res['id']
        return 0

    def update(self, item: Item) -> None:
        data = item.get_data()
        item_type = self.__get_item_type_name(item)
        data['type'] = item_type

        self.__do_request(requests.put, str(item.id), data)

    def delete(self, id: int) -> bool:
        res = self.__do_request(requests.delete, str(id))
        return res is not None

    def clear(self) -> bool:
        res = self.__do_request(requests.delete)
        return res is not None

    def __get_item_type_name(self, item: Item) -> str:
        if isinstance(item, Student):
            return "student"
        elif isinstance(item, Employee):
            return "employee"
        else:
            raise ValueError('Некорректный тип объекта')
