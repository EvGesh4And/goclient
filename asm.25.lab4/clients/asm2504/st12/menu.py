from .starosta import Starosta
from .proforg import Proforg


def run_menu(group):
    while True:
        print("\n=== МЕНЮ УПРАВЛЕНИЯ ГРУППОЙ ===")
        print("1. Добавить студента")
        print("2. Добавить старосту")
        print("3. Добавить профорга")
        print("4. Редактировать студента")
        print("5. Удалить студента")
        print("6. Показать всех студентов")
        print("7. Сохранить в файл/REST")
        print("8. Загрузить из файла/REST")
        print("9. Очистить группу")
        print("0. Выход")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            group.add_item()
        elif choice == "2":
            group.add_item(Starosta)
        elif choice == "3":
            group.add_item(Proforg)
        elif choice == "4":
            try:
                number = int(input("Введите номер студента для редактирования: "))
                group.edit_item(number - 1)
            except Exception:
                print("Ошибка: введите корректный номер")
        elif choice == "5":
            try:
                number = int(input("Введите номер студента для удаления: "))
                group.delete_item(number - 1)
            except Exception:
                print("Ошибка: введите корректный номер")
        elif choice == "6":
            group.list_items()
        elif choice == "7":
            filename = input("Введите имя файла для сохранения (например, data.pkl) или оставьте пустым для REST: ").strip()
            group.save(filename or None)
        elif choice == "8":
            filename = input("Введите имя файла для загрузки (например, data.pkl) или оставьте пустым для REST: ").strip()
            group.load(filename or None)
        elif choice == "9":
            confirm = input("Вы уверены, что хотите очистить группу? (y/n): ").strip().lower()
            if confirm in ["y", "yes", "д", "да"]:
                group.clear()
            else:
                print("Отмена")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

