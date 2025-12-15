try:
    from .group import group
except Exception:
    try:
        from group import group
    except Exception:
        group = None

def main():
    try:
        if group is not None:
            group().f()
    except Exception:
        pass

    run_app()

from .console_io import ConsoleIO
from .group_container import GroupContainer
from .rest_storage import RestStorage

DEFAULT_BASE_URL = "http://127.0.0.1:5000"
MODULE_HINT = "[2501-14]"


def create_storage(type_registry):
    base_url = input(f"URL сервера (Enter — {DEFAULT_BASE_URL}): ").strip() or DEFAULT_BASE_URL
    try:
        storage = RestStorage(base_url=base_url, module_hint=MODULE_HINT, type_registry=type_registry)
        storage.name = f"REST API ({base_url})"
        print(f"REST-хранилище готово. Маршрут: {storage.prefix}")
        return storage
    except RuntimeError as exc:
        print(f"Ошибка: {exc}")
        raise


def run_app():
    io = ConsoleIO()
    container = GroupContainer(io=io, storage=None)
    type_registry = {cls.__name__: cls for cls in container.types.values()}
    storage = create_storage(type_registry)
    container.storage = storage

    print("Картотека сотрудников (Сотрудник / Менеджер / Директор)")
    actions = {
        "1": "Добавить объект",
        "2": "Редактировать объект",
        "3": "Удалить объект",
        "4": "Вывести весь список",
        "5": "Очистить список",
        "0": "Выход",
    }

    while True:
        print("\nМеню:")
        for key in actions:
            print(" " + key + ". " + actions[key])
        print(f"Текущее хранилище: {container.get_storage_name()}")

        choice = input("Ваш выбор: ").strip()

        if choice == "0":
            print("Пока!")
            break
        elif choice == "1":
            container.add_item()
        elif choice == "2":
            container.edit_item()
        elif choice == "3":
            container.remove_item()
        elif choice == "4":
            container.list_items()
        elif choice == "5":
            container.clear()
        else:
            print("Нет такого пункта.")

if __name__ == "__main__":
    main()
