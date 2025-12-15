import pickle


class PickleStorage:
    def save(self, items, filepath):
        if filepath is None:
            print("Для pickle необходимо указать имя файла")
            return
        try:
            with open(filepath, "wb") as file:
                pickle.dump(items, file)
            print(f"Данные сохранены в файл {filepath}")
        except Exception as exc:
            print(f"Ошибка при сохранении: {exc}")

    def load(self, filepath):
        if filepath is None:
            print("Для pickle необходимо указать имя файла")
            return []
        try:
            with open(filepath, "rb") as file:
                items = pickle.load(file)
            print(f"Данные загружены из файла {filepath}")
            return items
        except FileNotFoundError:
            print(f"Файл {filepath} не найден")
            return []
        except Exception as exc:
            print(f"Ошибка при загрузке: {exc}")
            return []

