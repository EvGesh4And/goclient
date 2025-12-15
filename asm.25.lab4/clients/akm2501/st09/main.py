import os
import requests
import json
from .containeritem import Container
from .consoleio import ConsoleIO
from .pickle_storage import PickleStorage
from .rest_storage import RESTStorage

def get_student_url(student_code="2501-09"):
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
    
    print("="*50)
    print("КАРТОТЕКА СПОРТЗАЛА - [2501-09] Исламов")
    print("="*50)
    
    print("\nВыберите режим работы:")
    print("1. REST API (работа с сервером)")
    print("2. Локальное хранение (файлы)")
    
    mode_choice = input("Ваш выбор [1]: ").strip() or "1"
    
    if mode_choice == "1":
        base_url = get_student_url("2501-09")
        
        if not base_url:
            print("Не удалось найти URL для st09. Проверьте:")
            print("1. Запущен ли сервер (lab4.py)")
            print("2. Добавлен ли st09 в app/__init__.py")
            print("\nПереключаюсь на локальный режим...")
            storage_strategy = PickleStorage()
            use_rest = False
            filename = os.path.join(os.path.dirname(__file__), "gym_data.pkl")
        else:
            print(f"Подключение к серверу: {base_url}")
            storage_strategy = RESTStorage()
            storage_strategy.initialize(base_url)
            use_rest = True
            filename = None
    else:
        storage_strategy = PickleStorage()
        use_rest = False
        filename = os.path.join(os.path.dirname(__file__), "gym_data.pkl")
    
    container = Container(storage_strategy, use_rest)
    
    if use_rest:
        container.read_from_file(None)
    else:
        container.read_from_file(filename)
    
    def add_item():
        print("\nВыберите тип объекта:")
        print("1. Гость")
        print("2. Тренер")
        try:
            item_type = int(input("Ваш выбор: "))
            container.add_item(item_type, console_io)
        except ValueError:
            print("Ошибка: введите число 1 или 2")
    
    def show_list():
        container.display_list(console_io)
    
    def save():
        if use_rest:
            container.write_to_file(None)
        else:
            container.write_to_file(filename)
    
    def load():
        if use_rest:
            container.read_from_file(None)
        else:
            container.read_from_file(filename)
    
    def clear():
        container.clear_list()
    
    def exit_program():
        print("До свидания!")
        exit()
    
    menu = [
        ["Добавить запись", add_item],
        ["Показать все записи", show_list],
        ["Сохранить", save],
        ["Загрузить", load],
        ["Очистить картотеку", clear],
        ["Выход", exit_program]
    ]
    
    while True:
        print("\n" + "="*30)
        print(f"ГЛАВНОЕ МЕНЮ (Режим: {'REST API' if use_rest else 'Локальный'})")
        print("="*30)
        for i, menu_item in enumerate(menu, 1):
            print(f"{i}. {menu_item[0]}")
        
        try:
            choice = int(input("\nВыберите действие: "))
            if 1 <= choice <= len(menu):
                menu[choice-1][1]()
            else:
                print("Неверный выбор! Попробуйте снова.")
        except ValueError:
            print("Ошибка: введите число от 1 до 6")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()