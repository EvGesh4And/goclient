if __name__ != '__main__':
    from .console_io import ConsoleIO
else:
    from console_io import ConsoleIO

class BaseEntity:
    def __init__(self, io_strategy=None):
        self.io_strategy = io_strategy or ConsoleIO()
        self.name = ""
        self.price = 0.0         # ₽
        self.calories = 0        # ккал
        self.ingredients = []    # list[str]

    def input_fields(self):
        self._input_name()
        self._input_price()
        self._input_calories()
        self._input_ingredients()

    def output_fields(self):
        self.io_strategy.output_field("Тип", self.__class__.__name__)
        self.io_strategy.output_field("Название", self.name)
        self.io_strategy.output_field("price", self.price)
        self.io_strategy.output_field("calories", self.calories)
        self.io_strategy.output_field("ingredients", self.ingredients)

    def edit_field_by_key(self, key: str):
        """Редактировать одно поле по ключу ('name'|'price'|'calories'|'ingredients')."""
        if key == "name":
            self._input_name()
        elif key == "price":
            self._input_price()
        elif key == "calories":
            self._input_calories()
        elif key == "ingredients":
            self._input_ingredients()
        else:
            print("Неизвестное поле.")

    def _input_name(self):
        while True:
            name = self.io_strategy.input_field("Введите название блюда: ").strip()
            if name:
                self.name = name
                break
            print("Название не может быть пустым.")

    def _input_price(self):
        while True:
            raw = self.io_strategy.input_field("Введите цену (руб): ").replace(",", ".").strip()
            try:
                price = float(raw)
                if price < 0:
                    print("Цена не может быть отрицательной.")
                else:
                    self.price = price
                    break
            except ValueError:
                print("Введите число (например, 250 или 199.99).")

    def _input_calories(self):
        while True:
            raw = self.io_strategy.input_field("Введите калорийность (ккал): ").strip()
            try:
                cal = int(raw)
                if cal < 0:
                    print("Калорийность не может быть отрицательной.")
                else:
                    self.calories = cal
                    break
            except ValueError:
                print("Введите целое число (например, 320).")

    def _input_ingredients(self):
        # Ввод через ЗАПЯТУЮ: 'томат, паста, сыр' -> ['томат','паста','сыр']
        raw_ing = self.io_strategy.input_field(
            "Введите ингредиенты через запятую (можно пусто): "
        ).strip()
        self.ingredients = [s.strip() for s in raw_ing.split(",") if s.strip()]

    # ----- Сериализация -----
    def to_dict(self):
        """Сериализация в dict для хранения."""
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'price': self.price,
            'calories': self.calories,
            'ingredients': self.ingredients,
        }

    @classmethod
    def from_dict(cls, data, io_strategy=None):
        """Десериализация из dict для разных типов блюд."""
        type_map = {
            'Soup': Soup,
            'MainCourse': MainCourse,
            'Dessert': Dessert,
            'Drink': Drink,
        }
        t = data.get('type')
        if t not in type_map:
            raise ValueError(f"Неизвестный тип блюда: {t}")
        obj = type_map[t](io_strategy)
        obj.name = data.get('name', '')
        obj.price = data.get('price', 0.0)
        obj.calories = data.get('calories', 0)
        obj.ingredients = data.get('ingredients', []) or []
        return obj


# ---- Типы блюд ----

class Soup(BaseEntity):
    pass


class MainCourse(BaseEntity):  # Горячее
    pass


class Dessert(BaseEntity):
    pass


class Drink(BaseEntity):
    pass
