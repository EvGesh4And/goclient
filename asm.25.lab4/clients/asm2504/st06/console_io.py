"""
Стратегия ввода/вывода для консоли.
Реализует методы input_field(obj, field_name, prompt, current) и output_field(obj, field_name).
"""

from typing import Any

class ConsoleIO:
    def input_field(self, obj: Any, field_name: str, prompt: str, current_value=None):
        """
        Запрашивает значение у пользователя для поля field_name.
        Пытается привести ввод к типу текущего значения (если он не None),
        либо оставляет как строку.
        """
        if current_value is None or current_value == '':
            default = ''
        else:
            default = f" [{current_value}]"
        raw = input(f"{prompt}{default}: ").strip()
        if raw == '':
            # если пустой ввод — возвращаем текущее значение
            return current_value
        # Попытка приведения по типу текущего значения
        if isinstance(current_value, bool):
            low = raw.lower()
            return low in ('1','y','yes','true','t','да','д')
        if isinstance(current_value, int):
            try:
                return int(raw)
            except ValueError:
                print("Неверный ввод — должно быть целое число. Оставлю текущее значение.")
                return current_value
        if isinstance(current_value, float):
            try:
                return float(raw)
            except ValueError:
                print("Неверный ввод — должно быть число. Оставлю текущее значение.")
                return current_value
        # по умолчанию — строка
        return raw

    def output_field(self, obj: Any, field_name: str, prompt: str = None):
        """Выводит значение поля объекта на экран."""
        if prompt is None:
            prompt = field_name
        value = getattr(obj, field_name, None)
        print(f"{prompt}: {value}")
