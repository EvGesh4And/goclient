from entities.student import Student
from entities.teacher import Teacher
from entities.staff import Staff

class University:
    def __init__(self, storage_strategy=None):
        self.people = []
        self.storage_strategy = storage_strategy

    def add_person(self, io_strategy):
        print("Выберите тип объекта:\n1. Student\n2. Teacher\n3. Staff")
        choice = input("Ваш выбор: ")
        cls_map = {"1": Student, "2": Teacher, "3": Staff}
        cls = cls_map.get(choice)
        if not cls:
            print("Неверный выбор.")
            return
        obj = cls(io_strategy=io_strategy)
        obj.input_data()
        self.people.append(obj)

    def show_all(self):
        if not self.people:
            print("Список пуст.")
        for idx, person in enumerate(self.people, start=1):
            print(f"{idx}. {person}")

    def edit_person(self):
        self.show_all()
        if not self.people:
            return
        idx = int(input("Введите номер объекта для изменения: ")) - 1
        if 0 <= idx < len(self.people):
            person = self.people[idx]
            print("Доступные поля:", [a for a in vars(person) if a != "io_strategy"])
            field = input("Введите имя поля для изменения: ")
            value = input("Введите новое значение: ")
            person.edit_field(field, value)
        else:
            print("Неверный индекс!")

    def remove_person(self):
        self.show_all()
        if not self.people:
            return
        idx = int(input("Введите номер для удаления: ")) - 1
        if 0 <= idx < len(self.people):
            removed = self.people.pop(idx)
            print(f"Удалён: {removed}")
        else:
            print("Неверный индекс!")

    def clear(self):
        self.people.clear()
        print("Список очищен.")

    def save_to_file(self, filename):
        if self.storage_strategy:
            self.storage_strategy.save(filename, self.people)

    def load_from_file(self, filename):
        if self.storage_strategy:
            self.people = self.storage_strategy.load(filename)
