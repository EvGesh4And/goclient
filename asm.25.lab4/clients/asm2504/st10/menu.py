from .container import Container
from .strategy_console_io import ConsoleIO
from .strategy_storage_pickle import PickleStorage
from .strategy_storage_sqlite import SQLiteStorage
from .strategy_storage_REST import RESTStorage
from .student_bachelor import StudentBachelor
from .student_master import StudentMaster
from .student_graduate import StudentGraduate
from typing import List
import os

def menu():    
    CLASS_LIST: List[type] = [StudentBachelor, StudentMaster, StudentGraduate]
    cont = Container(
    io_strategy=ConsoleIO(classes=CLASS_LIST),
    storage_strategy=RESTStorage(base_url=get_url_storage(), classes=CLASS_LIST),
    classes=CLASS_LIST)
    
    while True:
        actions = {
            "1": ("Добавить студента", lambda: add_object_ui(cont)),
            "2": ("Редактировать студента", lambda: edit_object_ui(cont)),
            "3": ("Удалить студента", lambda: remove_object_ui(cont)),
            "4": ("Вывести весь список", lambda: cont_output_ui(cont)),
            "5": ("Сохранить в файл", lambda: save_ui(cont)),
            "6": ("Загрузить из файла", lambda: load_ui(cont)),
            "7": ("Очистить список", cont.clear_with_message),
            "8": (f"Стратегия хранения: {cont.storage.__class__.__name__}", lambda: set_storage(cont)),
            "0": ("Выход", None)
        }
        cont.io.output_message("\nМеню:")
        for k, (desc, _) in actions.items():
            cont.io.output_message(f"{k}. {desc}")
        choice = cont.io.input_raw("Выберите действие: ")
        if choice == "0":
            cont.io.output_message("Выход")
            break
        act = actions.get(choice)
        if not act:
            cont.io.output_message("Отсуствует данная функция")
            continue
        _, func = act
        if func:
            func()

def get_path_storage():
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    NUM_DIR = int(str(THIS_DIR).split(os.sep)[-1][2:])
    PROJECT_APP_DIR = os.path.abspath(os.path.join(THIS_DIR, '..', '..'))
    STORAGE_DIR = os.path.join(PROJECT_APP_DIR, '..', 'data', 'asm2504', f'st{NUM_DIR}', 'client')
    return STORAGE_DIR

import requests
def get_url_storage():
    resp = requests.Session().get("http://127.0.0.1:5000/api/", timeout=5)
    resp.raise_for_status()
    data = resp.json()
    for index, title in data.get("sts", []) if isinstance(data, dict) else []:
        if isinstance(title, str) and "Князев" in title:
            return f"http://127.0.0.1:5000/st{index}/api"
        
def set_storage(cont):
    type_storage = {
    "1": "Pickle",
    "2": "SQLite",
    "3": "REST",
    "0": "Отмена"
    }
    for k, desc in type_storage.items():
        cont.io.output_message(f"{k}. {desc}")
    choice = cont.io.input_raw("Выберите тип хранения: ")
    if choice == "0" or not choice:
        cont.io.output_message("Выход" if choice == "0" else "Отсутствует данная стратегия")
        return
    new_storage = type_storage.get(choice)
    current = cont.storage.__class__.__name__ if cont.storage is not None else None

    if new_storage and new_storage != current:
        new_store = None

        if new_storage == "Pickle":
            new_store = PickleStorage(base_dir=get_path_storage(), classes=cont.classes,
                                    items=cont.list_items_with_message())

        elif new_storage == "SQLite":
            new_store = SQLiteStorage(base_dir=get_path_storage(), classes=cont.classes,
                                    items=cont.list_items_with_message())

        elif new_storage == "REST":
            new_store = RESTStorage(base_url=get_url_storage(), classes=cont.classes)

        if new_store is not None:
            cont.storage = new_store
            cont.io.output_message(f'Стратегия изменена на {new_storage}')
        else:
            cont.io.output_message('Не удалось создать новое хранилище')
    else:
        cont.io.output_message(f'Оставлена та же стратегия: {current}')
    
def add_object_ui(cont: Container):
    type_idx = cont.io.select_type()
    if type_idx is None:
        return
    cls = cont.classes[type_idx]
    raw_fields = cont.io.input_fields(cls())
    cont.create_from_type_index(type_idx, raw_fields)

def edit_object_ui(cont: Container):
    items = cont.list_items_with_message()
    if not items:
        return
    idx = cont.io.select_index(items)
    if idx is None:
        return
    obj = items[idx]
    updates = cont.io.input_updates(obj)
    if not updates:
        return
    cont.edit_by_index_str(str(idx), updates)

def remove_object_ui(cont: Container):
    items = cont.list_items_with_message()
    if not items:
        return
    idx = cont.io.select_index(items)
    if idx is None:
        return
    cont.remove_by_index_str(str(idx))

def cont_output_ui(cont: Container):
    items = cont.list_items_with_message()
    if not items:
        return
    for i, obj in enumerate(items):
        cont.io.output_message(f"[{i}] {obj}")

def save_ui(cont: Container):
    fname = cont.io.input_raw("Имя файла для сохранения: ")
    if fname:
        cont.save_by_filename(fname)

def load_ui(cont: Container):
    fname = cont.io.input_raw("Имя файла для загрузки: ")
    if fname:
        cont.load_by_filename(fname)
