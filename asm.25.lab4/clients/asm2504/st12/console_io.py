class ConsoleIO:
    def input_field(self, obj, field_name, field_type):
        current_value = getattr(obj, field_name, "")

        prompts = {
            "name": "Введите имя и фамилию",
            "age": "Введите возраст (целое число)",
            "group": "Введите группу (например, ИУ5-32)",
            "record_book": "Введите номер зачетной книжки",
            "avg_grade": "Введите средний балл (0-5)",
            "phone": "Введите телефон",
            "duties": "Введите обязанности",
            "union_member": "Член профсоюза? (y/n)",
            "events_count": "Количество организованных мероприятий",
        }
        prompt = prompts.get(field_name, f"Введите {field_name}")

        if current_value != "":
            print(f"{prompt} (текущее: {current_value}): ", end="")
        else:
            print(f"{prompt}: ", end="")

        user_input = input().strip()

        if user_input == "" and current_value != "":
            return

        try:
            if field_type == str:
                value = user_input
            elif field_type == int:
                value = int(user_input)
            elif field_type == float:
                value = float(user_input)
            elif field_type == bool:
                value = user_input.lower() in ["y", "yes", "1", "true", "д", "да", "+"]
            else:
                value = user_input

            if hasattr(obj, "validate"):
                value = obj.validate(field_name, value)

            setattr(obj, field_name, value)
        except ValueError as exc:
            print(f"Ошибка ввода: {exc}")
            print("Попробуйте еще раз")
            self.input_field(obj, field_name, field_type)
        except Exception as exc:
            print(f"Ошибка: {exc}")
            print("Попробуйте еще раз")
            self.input_field(obj, field_name, field_type)

    def print_field(self, obj, field_name):
        value = getattr(obj, field_name, "не задано")
        labels = {
            "name": "Имя",
            "age": "Возраст",
            "group": "Группа",
            "record_book": "Зачетная книжка",
            "avg_grade": "Средний балл",
            "phone": "Телефон",
            "duties": "Обязанности",
            "union_member": "Член профсоюза",
            "events_count": "Организовано мероприятий",
        }
        label = labels.get(field_name, field_name)
        if field_name == "union_member":
            value = "да" if value else "нет"
        print(f"{label}: {value}")

