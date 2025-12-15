import os
import requests
import json
from .containeritem import Container
from .consoleio import ConsoleIO
from .picklestorage import PickleStorage
from .rest_storage import RESTStorage

def get_student_url(student_code="2501-03"):
    try:
        response = requests.get("http://localhost:5000/api/")
        if response.status_code == 200:
            data = response.json()
            for i, title in data['sts']:
                if student_code in title:
                    return f"http://localhost:5000/st{i}"
            print(f"Студент {student_code} не найден в списке")
            return None
        else:
            print("Не удалось получить список студентов")
            return None
    except Exception as e:
        print(f"Ошибка подключения к серверу: {e}")
        return None

def main():
    console_io = ConsoleIO()
    
    base_url = get_student_url("2501-03")
    
    if not base_url:
        print("Используется локальное хранилище")
        use_rest = False
        filename = os.path.join(os.path.dirname(__file__), "cardfile.pkl")
        storage_strategy = PickleStorage()
    else:
        print(f"Найден URL: {base_url}")
        storage_strategy = RESTStorage()
        storage_strategy.initialize(base_url)
        use_rest = True
    
    container = Container(storage_strategy, use_rest)
    filename = os.path.join(os.path.dirname(__file__), "cardfile.pkl")
    
    def add_item():
        print("\nВыберите тип объекта:")
        print("1. Person (Человек)")
        print("2. Worker (Работник)")
        print("3. Hobby (Хобби)")
        item_type = int(input("Ваш выбор: "))
        container.add_item(item_type, console_io)
    
    def show_list():
        container.display_list(console_io)
    
    def save():
        container.sync_with_server()
    
    def load():
        container.read_from_file(filename)
    
    def clear():
        container.clear_list()
    
    def exit_program():
        print("До свидания!")
        exit()
    
    menu = [
        ["Добавить", add_item],
        ["Показать", show_list],
        ["Сохранить", save],
        ["Загрузить", load],
        ["Очистить", clear],
        ["Выход", exit_program]
    ]
    
    while True:
        print("\n" + "="*20)
        print(f"КАРТОТЕКА (REST: {use_rest})")
        print("="*20)
        for i, menu_item in enumerate(menu, 1):
            print(f"{i}. {menu_item[0]}")
        try:
            m = int(input())
            menu[m-1][1]()
        except (ValueError, IndexError):
            print("Неверный выбор! Попробуйте снова.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()