from collections.abc import Callable
from typing import Dict

from .card_index import CardIndex


class Menu:
    def __init__(self, card_index: CardIndex):
        self.__card_index = card_index

        self.__is_running = True

        self.__options: Dict[int, tuple[str, Callable]] = {
            1: ("Добавить", self.__add),
            2: ("Удалить", self.__delete),
            3: ('Показать', self.__show),
            4: ("Очистить", self.__clear),
            5: ('Выход', self.__exit)
        }

    def run(self):
        while self.__is_running:
            print('----- КАРТОТЕКА -----')

            for number in sorted(self.__options):
                title = self.__options[number][0]
                print(f'{number}: {title}')

            input_data = input('Выберите пункт меню: ')

            action = None

            if input_data.isdigit():
                option_number = int(input_data)
                action = self.__options.get(option_number)

            if action is not None:
                action[1]()
            else:
                print('Неизвестный пункт меню')
            print()

    def __add(self):
        self.__card_index.add()

    def __delete(self):
        self.__card_index.delete()

    def __clear(self):
        self.__card_index.clear()

    def __show(self):
        self.__card_index.show()

    def __exit(self):
        self.__card_index.store()
        self.__is_running = False