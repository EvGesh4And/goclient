import requests
from flask import json

from .pickle_storage import PickleStorage
from .group import Group
from .console_handler import ConsoleIOHandler
from .rest_storage import RestStorage


def get_path(self):
    try:
        url = f'http://127.0.0.1:5000/api/'
        header = None
        res = requests.get(url, headers=header)
        if res.status_code == 200:
            if res.content:
                return json.loads(res.content)
            else:
                return None
    except Exception as ex:
        print(ex)

def main():
    group = Group(RestStorage(), ConsoleIOHandler())
    def add_item():
        for type, value in group.classes.items():
            print(f"{type}: {value.__name__}")
        id = input("Выберите тип: ")
        if id in group.classes:
            cls = group.classes[id]
            group.add(cls)
        else:
            print("Введено некорректное значение")

    def edit_item():
        id = int(input("Введите id сотрудника:"))
        item = group.get_item(id)
        if item is not None:
            item.io_handler = ConsoleIOHandler()
            item.input()
            group.edit(item)
        else:
            print("Введено некорректное значение")

    def delete_item():
        id = int(input("Введите id сотрудника:"))
        group.delete(id)

    menu = {
        "1": add_item,
        "2": edit_item,
        "3": delete_item,
        "4": group.show_items,
        "5": group.save,
        "6": group.load,
        "7": group.clear,
        "0": exit,
    }

    while True:
        print("\nМеню:")
        print("1 - Добавить объект")
        print("2 - Редактировать объект")
        print("3 - Удалить объект")
        print("4 - Показать список")
        print("5 - Сохранить в файл")
        print("6 - Загрузить из файла")
        print("7 - Очистить список")
        print("0 - Выход")

        choice = input("Выберите действие: ")
        action = menu.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()
