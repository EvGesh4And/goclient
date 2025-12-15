from ..entities.student import Student
from ..entities.teacher import Teacher
from ..entities.staff import Staff

class University:
    def __init__(self, storage_strategy=None):
        self.people = []
        self.storage_strategy = storage_strategy

    def add_person(self, io_strategy):
        print("\nВыберите тип объекта:")
        print("1. Student")
        print("2. Teacher") 
        print("3. Staff")
        
        choice = input("Ваш выбор: ").strip()
        cls_map = {"1": Student, "2": Teacher, "3": Staff}
        cls = cls_map.get(choice)
        
        if not cls:
            print(" Неверный выбор.")
            return
        
        obj = cls(io_strategy=io_strategy)
        obj.input_data()
        self.people.append(obj)
        
        
        if self.storage_strategy and hasattr(self.storage_strategy, 'add'):
            if self.storage_strategy.add(obj):
                print(" Объект добавлен и отправлен на сервер!")
            else:
                print(" Объект добавлен локально, но ошибка отправки на сервер")
        else:
            print(" Объект успешно добавлен!")

    def show_all(self):
        if not self.people:
            print(" Список пуст.")
            return
        
        print(f"\n{'='*60}")
        print(f"{'№':<3} {'Тип':<10} {'Имя':<15} {'Возраст':<8} {'Доп. информация'}")
        print(f"{'='*60}")
        
        for idx, person in enumerate(self.people, start=1):
            if isinstance(person, Student):
                info = f"Факультет: {person.faculty}, Группа: {person.group}"
            elif isinstance(person, Teacher):
                info = f"Кафедра: {person.department}, Должность: {person.position}"
            elif isinstance(person, Staff):
                info = f"Отдел: {person.department}, Должность: {person.position}"
            else:
                info = ""
            
            print(f"{idx:<3} {person.__class__.__name__:<10} {person.name:<15} {person.age:<8} {info}")

    def edit_person(self):
        self.show_all()
        if not self.people:
            return
        
        try:
            idx = int(input("Введите номер объекта для изменения: ")) - 1
            if 0 <= idx < len(self.people):
                person = self.people[idx]
                print(f"\nРедактирование: {person}")
                print("Доступные поля:", [a for a in vars(person) if a not in ("io_strategy", "_io_strategy")])
                
                field = input("Введите имя поля для изменения: ").strip()
                value = input("Введите новое значение: ").strip()
                
                person.edit_field(field, value)
                print(" Объект изменен!")
            else:
                print(" Неверный индекс!")
        except ValueError:
            print(" Введите корректный номер!")
        except Exception as e:
            print(f" Ошибка: {e}")

    def remove_person(self):
        self.show_all()
        if not self.people:
            return
        
        try:
            idx = int(input("Введите номер для удаления: ")) - 1
            if 0 <= idx < len(self.people):
                removed = self.people.pop(idx)
                print(f" Удалён: {removed}")
            else:
                print(" Неверный индекс!")
        except ValueError:
            print(" Введите корректный номер!")

    def clear(self):
        self.people.clear()
        print(" Список очищен.")

    def save_to_file(self, filename="university_data.pkl"):
        if self.storage_strategy:
            self.storage_strategy.save(filename, self.people)

    def load_from_file(self, filename="university_data.pkl"):
        if self.storage_strategy:
            loaded_data = self.storage_strategy.load(filename)
            if loaded_data:
                self.people = loaded_data
                print(f" Загружено {len(self.people)} записей")