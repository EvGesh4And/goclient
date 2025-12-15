import os
from .group import Group
from .rest_storage import RestStorage


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    print("=" * 50)
    print("     КЛИЕНТ ДЛЯ МЕНЮ =)")
    print("=" * 50)

    print("\nВыберите режим работы:")
    print("1. PICKLE")
    print("2. REST API")
    print("3. Выход")

    mode = input("\nВаш выбор (1-3): ").strip()

    if mode == "3":
        return

    use_rest = (mode == "2")

    if use_rest:
        print(f"\nПодключение к REST API...")
        print("=" * 50)
        rest_storage = RestStorage()
        menu = Group(use_rest=True)
    else:
        print("\nPICKLE")
        print("=" * 50)
        menu = Group(use_rest=False)

    menu.f()

    actions = {
        "1": menu.add,
        "2": menu.show_all,
        "3": menu.edit,
        "4": menu.delete,
        "5": menu.save,
        "6": menu.load,
        "7": menu.clear
    }

    while True:
        clear_screen()
        print("✤" * 40)
        print("               МЕНЮ")
        print("✤" * 40)
        print("Режим: " + ("REST API" if use_rest else "PICKLE"))
        if use_rest:
            print(f"Сервер: {rest_storage.base_url}")
        print("-" * 40)
        print("1. Добавить блюдо")
        print("2. Показать все блюда")
        print("3. Редактировать блюдо")
        print("4. Удалить блюдо")
        print("5. Сохранить в файл")
        print("6. Загрузить из файла")
        print("7. Очистить список")
        print("0. Выход")
        print("-" * 40)

        choice = input("Выберите действие: ")

        if choice == "0":
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == '__main__':
    main()