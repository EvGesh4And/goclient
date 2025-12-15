import pickle

class PickleStorage:
    def save(self, filename, data):
        with open(filename, "wb") as f:
            pickle.dump(data, f)
        print(f"Cписок сохранён в {filename}")

    def load(self, filename):
        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
            print(f"Список загружен из {filename}")
            return data
        except FileNotFoundError:
            print("Файл не найден.")
            return []
