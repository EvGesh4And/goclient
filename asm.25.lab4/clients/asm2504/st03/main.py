if __name__ == '__main__':
    from group import Group
    from pickle_storage import PickleStorage
    from rest_storage import RestStorage
else:
    from .group import Group
    from .pickle_storage import PickleStorage
    from .rest_storage import RestStorage


def choose_storage():
    print("\nВыберите хранилище:")
    print("1. Локальный pickle-файл (ЛР1)")
    print("2. REST API (ЛР4)")
    choice = input("Ваш выбор: ").strip()

    if choice == "2":
        print("Используется REST API как хранилище.")
        return RestStorage()

    print("Используется локальный pickle-файл.")
    return PickleStorage()


def main():
    storage = choose_storage()
    group = Group(storage=storage)

    def require_non_empty() -> bool:
        if not getattr(group, "entities", None):
            print("Меню пусто.")
            return False
        return True

    def prompt_index(action: str):
        if not require_non_empty():
            return None
        try:
            raw = input(f"Индекс блюда для операции «{action}» (с 1): ").strip()
            idx = int(raw) - 1
            if idx < 0 or idx >= len(group.entities):
                print("Неверный индекс.")
                return None
            return idx
        except ValueError:
            print("Ожидается число.")
            return None

    menu_options = {
        '1': group.add_entity,
        '2': lambda: (lambda i: group.edit_entity(i) if i is not None else None)(prompt_index("редактировать")),
        '3': lambda: (lambda i: group.delete_entity(i) if i is not None else None)(prompt_index("удалить")),
        '4': group.display_list,
        '5': group.save_to_file,
        '6': group.load_from_file,
        '7': group.clear_list,
        '0': lambda: print("Выход.") or exit(0)
    }

    while True:
        print("\n=== Меню ресторана ===")
        print("1. Добавить блюдо")
        print("2. Редактировать блюдо")
        print("3. Удалить блюдо")
        print("4. Показать меню")
        print("5. Сохранить в файл/API")
        print("6. Загрузить из файла/API")
        print("7. Очистить меню")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        action = menu_options.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор.")


if __name__ == '__main__':
    main()