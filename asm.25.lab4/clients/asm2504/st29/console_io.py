class ConsoleIO:
    """Класс для консольного ввода/вывода"""

    def input_string(self, prompt):
        return input(f"{prompt}: ")

    def input_number(self, prompt):
        while True:
            try:
                return int(input(f"{prompt}: "))
            except ValueError:
                print("Ошибка! Введите целое число.")

    def input_float(self, prompt):
        while True:
            try:
                return float(input(f"{prompt}: "))
            except ValueError:
                print("Ошибка! Введите число.")

    def output(self, field_name, value):
        print(f"{field_name}: {value}")

    def output_message(self, message):
        print(message)

    def output_error(self, error_message):
        print(f"Ошибка: {error_message}")