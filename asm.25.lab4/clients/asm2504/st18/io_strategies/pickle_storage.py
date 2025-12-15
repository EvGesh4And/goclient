import pickle
import os

class PickleStorage:
    def save(self, filename, data):
        try:
            with open(filename, "wb") as f:
                pickle.dump(data, f)
            print(f"Список сохранён в файл: {filename}")
            print(f"   Количество записей: {len(data)}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load(self, filename):
        try:
            if not os.path.exists(filename):
                print(f" Файл {filename} не найден. Создан новый список.")
                return []
            
            with open(filename, "rb") as f:
                data = pickle.load(f)
            print(f"Список загружен из файла: {filename}")
            print(f"   Количество записей: {len(data)}")
            return data
        except Exception as e:
            print(f" Ошибка загрузки: {e}")
            return []