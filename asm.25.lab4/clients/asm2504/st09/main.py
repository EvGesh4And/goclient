if __name__ == '__main__':
    from group import Company
    from pickle_storage import PickleStorage
    from rest_storage import RestStorage
else:
    from .group import Company
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
    group = Company(storage=storage)

    actions = {
        "1": group.add_employee,
        "2": lambda: group.edit_employee(
            int(input("Введите номер сотрудника для редактирования (с 1): ")) - 1
            if group.employees else print("Список пуст.")
        ),
        "3": lambda: group.delete_employee(
            int(input("Введите номер сотрудника для удаления (с 1): ")) - 1
            if group.employees else print("Список пуст.")
        ),
        "4": group.display_list,
        "5": group.save_to_file,
        "6": group.load_from_file,
        "7": group.clear_list,
        "0": lambda: print("Завершение работы...") or exit(0),
    }

    while True:
        print("\n=== Меню компании ===")
        print("1. Добавить сотрудника")
        print("2. Редактировать сотрудника")
        print("3. Удалить сотрудника")
        print("4. Показать список сотрудников")
        print("5. Сохранить список в файл")
        print("6. Загрузить список из файла")
        print("7. Очистить список")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()
        action = actions.get(choice)

        if action:
            action()
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
