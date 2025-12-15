from .container.university import University
from .io_strategies.console import ConsoleIO
from .io_strategies.pickle_storage import PickleStorage
from .io_strategies.rest_storage import RESTStorage

def main():
    print("\n" + "="*50)
    print("          КАРТОТЕКА УНИВЕРСИТЕТА - LAB 4")
    print("="*50)
    
    print("\nВыберите режим работы:")
    print("1. Локальный режим (файлы .pkl)")
    print("2. REST режим (подключение к серверу)")
    print("="*50)
    
    while True:
        mode_choice = input("Ваш выбор (1 или 2): ").strip()
        if mode_choice in ["1", "2"]:
            break
        print("Неверный выбор! Введите 1 или 2")
    
    if mode_choice == "2":
        print("\n" + "="*50)
        print("          РЕЖИМ REST API")
        print("="*50)
        
        base_url = input(f"Введите URL сервера (по умолчанию http://127.0.0.1:5000): ").strip()
        if not base_url:
            base_url = "http://127.0.0.1:5000"
        
        try:
            storage = RESTStorage(base_url=base_url)
            print(f" Подключено к серверу: {base_url}")
            print(f"   Модуль: st{storage.student_number}")
        except Exception as e:
            print(f" Ошибка подключения: {e}")
            print(" Переключение в локальный режим")
            storage = PickleStorage()
    else:
        print("\n" + "="*50)
        print("          ЛОКАЛЬНЫЙ РЕЖИМ")
        print("="*50)
        storage = PickleStorage()
    
    university = University()
    io = ConsoleIO()
    
    university.storage_strategy = storage
    
    DEFAULT_FILENAME = "university_data.pkl"
    
    def save_to_file():
        if mode_choice == "2":
            print("\nСохранение на сервер...")
            university.save_to_file("")
        else:
            university.save_to_file(DEFAULT_FILENAME)
    
    def load_from_file():
        if mode_choice == "2":
            print("\n Загрузка с сервера...")
            university.load_from_file("")
        else:
            university.load_from_file(DEFAULT_FILENAME)
    
    def save_as():
        if mode_choice == "2":
            print(" В REST режиме имя файла не требуется")
            return
        
        filename = input(f"Введите имя файла (по умолчанию {DEFAULT_FILENAME}): ").strip()
        if not filename:
            filename = DEFAULT_FILENAME
        university.save_to_file(filename)
    
    def load_as():
        """Загрузить с указанием имени файла"""
        if mode_choice == "2":
            print(" В REST режиме имя файла не требуется")
            return
        
        filename = input(f"Введите имя файла (по умолчанию {DEFAULT_FILENAME}): ").strip()
        if not filename:
            filename = DEFAULT_FILENAME
        university.load_from_file(filename)
    
    menu_items = {
        "1": ("Добавить объект", lambda: university.add_person(io)),
        "2": ("Редактировать объект", university.edit_person),
        "3": ("Удалить объект", university.remove_person),
        "4": ("Вывести список", university.show_all),
        "5": ("Сохранить", save_to_file),
        "6": ("Сохранить как...", save_as) if mode_choice == "1" else ("6", None),
        "7": ("Загрузить", load_from_file),
        "8": ("Загрузить как...", load_as) if mode_choice == "1" else ("8", None),
        "9": ("Очистить список", university.clear),
        "0": ("Выход", exit)
    }
    
    #Убираем недоступные пункты меню
    if mode_choice == "2":
        if "6" in menu_items:
            del menu_items["6"]
        if "8" in menu_items:
            del menu_items["8"]
    
    while True:
        print("\n" + "="*50)
        print("          ГЛАВНОЕ МЕНЮ")
        if mode_choice == "2":
            print(f"          Режим: REST API")
            print(f"          Сервер: st{storage.student_number if hasattr(storage, 'student_number') else '?'}")
        else:
            print(f"          Режим: Локальный")
            print(f"          Файл: {DEFAULT_FILENAME}")
        print("="*50)
        
        for key, (description, _) in menu_items.items():
            print(f"{key}. {description}")
        
        print("="*50)
        
        choice = input("Выберите действие: ").strip()
        
        if choice in menu_items and menu_items[choice][1]:
            if choice == "0":
                print("\nДо свидания!")
                break
            
            try:
                menu_items[choice][1]()
            except KeyboardInterrupt:
                print("\n Операция прервана")
            except Exception as e:
                print(f" Ошибка: {e}")
        else:
            print(" Неверный выбор или функция недоступна!")