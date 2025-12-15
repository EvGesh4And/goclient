from pathlib import Path

try:
    from .models import Animal, Predator, Herbivore
    from .storage import DATA_DIR
except ImportError:  
    from models import Animal, Predator, Herbivore
    from storage import DATA_DIR

class PetShop:
    def __init__(self, io_strategy, storage_strategy):
        self.io = io_strategy
        self.storage = storage_strategy
        self.path: Path = DATA_DIR / "animals.db"
        self.load()

    def add_animal(self):
        animal_type = self.io.input("animal_type").lower()
        
        if animal_type == "predator":
            animal = Predator()
        elif animal_type == "herbivore":
            animal = Herbivore()
        else:
            animal = Animal()

        animal.input_data(self.io)
        self.storage.add(animal)
        self.save()
        return "Животное добавлено"

    def get_by_id(self, animal_id):
        return self.storage.get_by_id(animal_id)

    def show_catalog(self):
        return self.storage.get_all()

    def edit_animal(self, animal_id):
        animal = self.storage.get_by_id(animal_id)
        if animal:
            animal.input_data(self.io)
            self.storage.update_by_id(animal_id, animal)
            self.save()
            return "Животное изменено"
        return "Животное не найдено"

    def delete_animal(self, animal_id):
        if self.storage.get_by_id(animal_id):
            self.storage.delete_by_id(animal_id)
            self.save()
            return "Животное удалено"
        return "Животное не найдено"

    def save(self):
        self.storage.save(self.path)  
        return "Сохранено в файл"

    def load(self):
        try:
            self.storage.load(self.path)
            return "Загружено из файла"
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка загрузки: {e}"

    def clear_catalog(self):
        self.storage.clear()
        self.save()
        return "Каталог очищен"