try:
    from .group import group
except Exception:
    try:
        from group import group
    except Exception:
        group = None

from .console_io import ConsoleIO
from .container import Group
from .pickle_storage import PickleStorage
from .rest_storage import RestStorage
from .menu import run_menu

DEFAULT_BASE_URL = "http://127.0.0.1:5000"
MODULE_HINT = "[2504-12]"


def choose_storage():
    while True:
        print("Выберите хранилище:")
        print(" 1. Локальный pickle-файл")
        print(" 2. REST API (WSGI приложение)")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            storage = PickleStorage()
            print("Выбрано хранилище: PickleStorage (локальный файл)")
            return storage
        if choice == "2":
            base_url = input(f"URL сервера (Enter — {DEFAULT_BASE_URL}): ").strip() or DEFAULT_BASE_URL
            try:
                storage = RestStorage(base_url=base_url, module_hint=MODULE_HINT)
                prefix = storage.prefix
                print(f"REST-хранилище готово. Маршрут: {prefix}")
                return storage
            except RuntimeError as exc:
                print(f"Ошибка: {exc}")
        else:
            print("Нет такого варианта, попробуйте снова.")


def run_app():
    print("=== Система управления группой ===")
    storage = choose_storage()
    io = ConsoleIO()
    group_container = Group(storage, io)
    run_menu(group_container)


def main():
    try:
        if group is not None:
            group().f()
    except Exception:
        pass
    run_app()


if __name__ == "__main__":
    main()

