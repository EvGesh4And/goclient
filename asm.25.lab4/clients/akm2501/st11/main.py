try:
    from .group import group
except Exception:
    try:
        from group import group
    except Exception:
        group = None

from .console_io import ConsoleIO
from .group_container import GroupContainer
from .rest_storage import RestStorage

DEFAULT_BASE_URL = "http://127.0.0.1:5000"
MODULE_HINT = "[2501-11]"


def main():
    try:
        if group is not None:
            group().f()
    except Exception:
        pass

    run_app()


print("REST API (WSGI приложение)")
base_url = input(f"URL сервера (Enter — {DEFAULT_BASE_URL}): ").strip() or DEFAULT_BASE_URL


def choose_storage():
    """Выбор хранилища (только REST API)"""
    url = input(f"URL сервера (Enter — {base_url}): ").strip() or base_url
    try:
        storage = RestStorage(base_url=url, module_hint=MODULE_HINT)
        prefix = storage.prefix
        print(f"REST-хранилище готово. Маршрут: {prefix}")
        return storage
    except RuntimeError as exc:
        print(f"Ошибка: {exc}")
        return choose_storage()  # Повторная попытка


def run_app():
    io = ConsoleIO()
    storage = choose_storage()
    container = GroupContainer(io=io, storage=storage)

    print("Каталог животных (Animal / Predator / Herbivore)")
    actions = {
        "1": "Добавить запись",
        "2": "Редактировать запись",
        "3": "Удалить запись",
        "4": "Показать все записи",
        "5": "Сохранить в файл",
        "6": "Загрузить из файла",
        "7": "Очистить каталог",
        "8": "Сменить хранилище",
        "0": "Выход",
    }

    while True:
        print("\nМеню:")
        for key, title in actions.items():
            print(f" {key}. {title}")
        print(f"Текущее хранилище: {container.get_storage_name()}")

        choice = input("Ваш выбор: ").strip()

        if choice == "0":
            print("Пока!")
            break
        if choice == "1":
            container.add_item()
        elif choice == "2":
            container.edit_item()
        elif choice == "3":
            container.remove_item()
        elif choice == "4":
            container.list_items()
        elif choice == "5":
            path = input("Файл для сохранения (Enter — по умолчанию): ").strip()
            container.save(path or None)
        elif choice == "6":
            path = input("Файл для загрузки (Enter — по умолчанию): ").strip()
            container.load(path or None)
        elif choice == "7":
            container.clear()
        elif choice == "8":
            container.set_storage(choose_storage())
        else:
            print("Нет такого пункта.")


if __name__ == "__main__":
    main()

