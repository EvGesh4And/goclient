import pickle
import os

class PickleStorage:
    def __init__(self, filename="data/asm2504/st03/menu.pkl"):
        self.filename = filename

    def save(self, entities):
        """Сохранение списка объектов в бинарный файл."""
        if not entities:
            print("Меню пусто. Нечего сохранять.")
            return
        with open(self.filename, "wb") as f:
            pickle.dump(entities, f)
        print(f"Сохранено в {self.filename}")

    def load(self):
        """Загрузка списка объектов из файла."""
        if not os.path.exists(self.filename):
            print("Файл не найден.")
            return []
        with open(self.filename, "rb") as f:
            entities = pickle.load(f)
        print(f"Загружено из {self.filename}")
        return entities
