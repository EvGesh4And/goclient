if __name__ != '__main__':
    from .console_io import ConsoleIO
    from .container import Catalog
    from .storage_rest import StorageREST
else:
    from console_io import ConsoleIO
    from container import Catalog
    from storage_rest import StorageREST

def main():
    io = ConsoleIO()
    storage = StorageREST()  # REST как источник данных
    catalog = Catalog(io_strategy=io, storage_strategy=storage)

    # Подгружаем данные из REST при старте
    try:
        catalog._load_items_from_storage()
    except Exception as e:
        print("Не удалось загрузить данные из REST:", e)

    menu = {
        "1": ("Добавить объект", catalog.create_item_interactive),
        "2": ("Редактировать объект", catalog.edit_item),
        "3": ("Удалить объект", catalog.delete_item),
        "4": ("Вывести краткий список", catalog.list_summary),
        "5": ("Вывести полный список", catalog.print_full),
        "8": ("Очистить список", catalog.clear),
        "0": ("Выход", None),
    }

    while True:
        print("\n=== Клиент ASM2504-ST06 ===")
        for k, v in menu.items():
            print(f"{k}) {v[0]}")
        choice = input("Выбор: ").strip()
        if choice == "0":
            break
        action = menu.get(choice)
        if action and action[1]:
            try:
                action[1]()
            except Exception as e:
                print("Ошибка:", e)
        else:
            print("Неверный пункт.")

if __name__ == "__main__":
    main()
