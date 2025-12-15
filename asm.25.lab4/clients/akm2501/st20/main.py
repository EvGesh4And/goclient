from .consoleio import ConsoleIO
from .models import Nurse, Doctor
from .rest_storage import RestStorage

class MedicalInstitution:
    def __init__(self, storage):
        self.storage = storage
        self.io = ConsoleIO()
    
    def add_staff(self):
        print("\nВыберите тип медперсонала:")
        print("1. Медсестра")
        print("2. Врач")
        
        choice = self.io.input_data("Введите номер: ")
        
        if choice == "1":
            staff = Nurse()
        elif choice == "2":
            staff = Doctor()
        else:
            self.io.display_error("Неверный выбор")
            return
        
        staff.input_fields(self.io)
        
        if self.storage.add_item(staff):
            self.io.display_message("Сотрудник добавлен успешно!")
        else:
            self.io.display_error("Ошибка при добавлении сотрудника")
    
    def display_staff(self):
        items = self.storage.get_all_items()
        
        if not items:
            self.io.display_message("Картотека пуста")
            return
        
        print("\n=== МЕДИЦИНСКАЯ КАРТОТЕКА ===")
        for i, staff in enumerate(items, 1):
            print(f"\n--- {staff.get_type()} #{staff.id} ---")
            staff.output_fields(self.io)
        print("=" * 30)
        
        stats = self.storage.get_stats()
        if stats:
            print(f"\nСтатистика: Всего {stats.get('total', 0)} записей")
            print(f"Медсестер: {stats.get('nurses', 0)}")
            print(f"Врачей: {stats.get('doctors', 0)}")
    
    def edit_staff(self):
        try:
            item_id = int(self.io.input_data("Введите ID сотрудника для редактирования: "))
            item = self.storage.get_item(item_id)
            
            if not item:
                self.io.display_error("Сотрудник не найден")
                return
            
            print(f"\nРедактирование {item.get_type()} #{item.id}")
            print("Текущие данные:")
            item.output_fields(self.io)
            
            print("\nВведите новые данные (оставьте пустым для сохранения текущего):")
            
            old_values = {
                'name': item.name,
                'specialty': item.specialty,
                'category': item.category,
                'schedule': item.schedule
            }
            
            new_name = self.io.input_data(f"Имя [{item.name}]: ")
            if new_name:
                item.name = new_name
            
            new_specialty = self.io.input_data(f"Специальность [{item.specialty}]: ")
            if new_specialty:
                item.specialty = new_specialty
            
            new_category = self.io.input_data(f"Категория [{item.category}]: ")
            if new_category:
                item.category = new_category
            
            new_schedule = self.io.input_data(f"График работы [{item.schedule}]: ")
            if new_schedule:
                item.schedule = new_schedule
            
            if hasattr(item, 'procedure_room'):
                new_room = self.io.input_data(f"Процедурный кабинет [{item.procedure_room}]: ")
                if new_room:
                    item.procedure_room = new_room
                
                new_shift = self.io.input_data(f"Смена [{item.shift}]: ")
                if new_shift:
                    item.shift = new_shift
            
            if hasattr(item, 'license'):
                new_license = self.io.input_data(f"Лицензия [{item.license}]: ")
                if new_license:
                    item.license = new_license
                
                new_specialization = self.io.input_data(f"Специализация [{item.specialization}]: ")
                if new_specialization:
                    item.specialization = new_specialization
            
            if self.storage.update_item(item):
                self.io.display_message("Сотрудник обновлен успешно!")
            else:
                item.name = old_values['name']
                item.specialty = old_values['specialty']
                item.category = old_values['category']
                item.schedule = old_values['schedule']
                self.io.display_error("Ошибка при обновлении сотрудника")
                
        except ValueError:
            self.io.display_error("Неверный ID. Должно быть число.")
    
    def delete_staff(self):
        try:
            item_id = int(self.io.input_data("Введите ID сотрудника для удаления: "))
            
            confirm = self.io.input_data(f"Вы уверены, что хотите удалить сотрудника #{item_id}? (y/n): ")
            if confirm.lower() == 'y':
                if self.storage.delete_item(item_id):
                    self.io.display_message("Сотрудник удален успешно!")
                else:
                    self.io.display_error("Ошибка при удалении сотрудника")
            else:
                self.io.display_message("Удаление отменено")
                
        except ValueError:
            self.io.display_error("Неверный ID. Должно быть число.")
    
    def show_stats(self):
        stats = self.storage.get_stats()
        if stats:
            print("\n=== СТАТИСТИКА ===")
            print(f"Всего записей: {stats.get('total', 0)}")
            print(f"Медсестер: {stats.get('nurses', 0)}")
            print(f"Врачей: {stats.get('doctors', 0)}")
            print("=" * 30)
        else:
            self.io.display_error("Не удалось получить статистику")

def main():
    print("\n=== МЕДИЦИНСКАЯ КАРТОТЕКА (REST API) ===")
    print("Автоматическое подключение к веб-приложению...")
    
    # Создаем хранилище без указания URL - оно само определит
    storage = RestStorage()
    
    # Проверяем соединение
    print("Проверка соединения с сервером...")
    try:
        test_items = storage.get_all_items()
        print(f"✓ Соединение установлено")
        print(f"  Записей на сервере: {len(test_items)}")
    except Exception as e:
        print(f"✗ Не удалось подключиться к серверу")
        print(f"  Ошибка: {e}")
        print("\nУбедитесь, что веб-сервер запущен:")
        print("  1. Откройте другое окно терминала")
        print("  2. Запустите: python lab4.py")
        print("  3. Нажмите Enter для продолжения...")
        input()
    
    institution = MedicalInstitution(storage)
    
    while True:
        print("\n=== МЕНЮ ===")
        print("1. Добавить сотрудника")
        print("2. Показать всех сотрудников")
        print("3. Редактировать сотрудника")
        print("4. Удалить сотрудника")
        print("5. Показать статистику")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            institution.add_staff()
        elif choice == "2":
            institution.display_staff()
        elif choice == "3":
            institution.edit_staff()
        elif choice == "4":
            institution.delete_staff()
        elif choice == "5":
            institution.show_stats()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()