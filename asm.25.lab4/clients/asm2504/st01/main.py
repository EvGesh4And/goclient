if __name__ == '__main__':
    from group import Group
else:
    from .group import Group
import requests


def get_api_url():
    my_name = "[2504-01] Алешко"
    try:
        response = requests.get("http://127.0.0.1:5000/api/", timeout=1)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('sts', []):
                # item expected like [num, name]
                try:
                    if my_name in item[1]:
                        found_url = f"http://127.0.0.1:5000/st{item[0]}/"
                        return found_url
                except Exception:
                    continue
    except Exception as e:
        print(f"API discovery error: {e}")
    return None

def main():
    default_api = 'http://127.0.0.1:5000/st01/api/'
    discovered = get_api_url()
    if discovered:
        default_api = discovered.rstrip('/') + '/api/'

    group = Group(storage_type='rest')
    try:
        group.storage = group.storage.__class__(default_api)
    except Exception:
        pass

    try:
        group.pull_from_api()
    except Exception:
        print('Не удалось загрузить данные с API при старте.')

    def safe_int_input(prompt):
        try:
            return int(input(prompt))
        except Exception:
            return None

    menu_options = {
        '1': group.add_entity,
        '2': lambda: (print('Список пуст.') if not group.entities else group.edit_entity_by_id(safe_int_input('ID для редактирования: '))),
        '3': lambda: (print('Список пуст.') if not group.entities else group.delete_entity_by_id(safe_int_input('ID для удаления: '))),
        '4': group.display_list,
        '5': group.export_to_file,
        '6': group.import_from_file,
        '7': group.clear_list,
        '0': lambda: exit(0)
    }

    while True:
        print('\n=== Меню картотеки ===')
        print('1. Добавить карточку')
        print('2. Редактировать карточку')
        print('3. Удалить карточку')
        print('4. Вывести список')
        print('5. Экспорт в локальный файл (фиксированное имя)')
        print('6. Импорт из локального файла (фиксированное имя)')
        print('7. Очистить список (и в хранилище, если REST)')
        print('0. Выход')
        choice = input('Выберите действие: ').strip()
        action = menu_options.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f'Ошибка при выполнении действия: {e}')
        else:
            print('Неверный выбор.')


if __name__ == '__main__':
    main()

