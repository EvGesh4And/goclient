from .student import Student
from .starosta import Starosta
from .proforg import Proforg


class Group:
    def __init__(self, storage, io):
        self.storage = storage
        self.io = io
        self.items = []
        # Auto-load from REST API if using RestStorage
        if self._is_rest_storage():
            try:
                self.load(None)
                print(f"✓ Данные загружены с сервера ({len(self.items)} записей)")
            except Exception as e:
                print(f"⚠ Не удалось загрузить данные с сервера: {e}")
                print("Продолжаем работу с пустым списком")

    def _is_rest_storage(self):
        """Check if storage is RestStorage"""
        return hasattr(self.storage, '_students_url') or type(self.storage).__name__ == 'RestStorage'

    def _auto_sync_rest(self):
        """Automatically sync with REST API after changes"""
        if self._is_rest_storage():
            try:
                self.storage.save(self.items, None)
                print("✓ Изменения синхронизированы с сервером")
            except Exception as e:
                print(f"⚠ Ошибка синхронизации с сервером: {e}")

    def add_item(self, student_type=None):
        if student_type is None:
            print("Выберите тип добавляемого объекта:")
            print("1. Student (Студент)")
            print("2. Starosta (Староста)")
            print("3. Proforg (Профорг)")
            choice = input("Ваш выбор (1-3): ").strip()
            if choice == "1":
                student_type = Student
            elif choice == "2":
                student_type = Starosta
            elif choice == "3":
                student_type = Proforg
            else:
                print("Неверный выбор")
                return

        new_student = student_type()
        new_student.io = self.io
        print(f"Ввод данных для {new_student.__class__.__name__}:")
        new_student.input_fields()
        self.items.append(new_student)
        print("Объект добавлен в группу")
        # Auto-sync with REST API if using it
        if self._is_rest_storage():
            self._auto_sync_rest()

    def list_items(self):
        # Auto-reload from REST API if using it
        if self._is_rest_storage():
            try:
                self.load(None)
            except Exception:
                pass

        if not self.items:
            print("Группа пуста")
            return

        print("Список студентов в группе:")
        for i, student in enumerate(self.items, start=1):
            print(f"\n--- Студент #{i} ({student.__class__.__name__}) ---")
            student.print_fields()
        print("\n--- Конец списка ---")

    def edit_item(self, index):
        # Auto-reload from REST API if using it
        if self._is_rest_storage():
            try:
                self.load(None)
            except Exception:
                pass

        if index < 0 or index >= len(self.items):
            print("Нет такого номера")
            return

        student = self.items[index]
        student.io = self.io
        print(f"Редактирование студента #{index + 1} ({student.__class__.__name__})")
        print("1. Ввести все поля заново")
        print("2. Изменить одно поле")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            student.input_fields()
            print("Все поля обновлены")
        elif choice == "2":
            student.edit_single_field()
        else:
            print("Отмена редактирования")
            return

        # Auto-sync with REST API if using it
        if self._is_rest_storage():
            self._auto_sync_rest()

    def delete_item(self, index):
        # Auto-reload from REST API if using it
        if self._is_rest_storage():
            try:
                self.load(None)
            except Exception:
                pass

        if index < 0 or index >= len(self.items):
            print("Нет такого номера")
            return
        student = self.items[index]
        print(f"Удаляем студента #{index + 1}: {student.name}")
        del self.items[index]
        print("Студент удален")
        # Auto-sync with REST API if using it
        if self._is_rest_storage():
            self._auto_sync_rest()

    def clear(self):
        self.items = []
        print("Группа очищена")
        # Auto-sync with REST API if using it
        if self._is_rest_storage():
            self._auto_sync_rest()

    def save(self, filepath):
        self.storage.save(self.items, filepath)

    def load(self, filepath):
        self.items = self.storage.load(filepath)
        for student in self.items:
            student.io = self.io

