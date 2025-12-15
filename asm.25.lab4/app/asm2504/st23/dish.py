from .console_io import ConsoleIO


class Dish:
    field_labels = {
        "name": "Название блюда",
        "cuisine": "Кухня (страна)",
        "calories": "Калории"
    }

    def __init__(self, io_strategy=None):
        self.name = ""
        self.cuisine = ""
        self.calories = 0
        self.io_strategy = io_strategy or ConsoleIO()

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'io_strategy' in state:
            del state['io_strategy']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if not hasattr(self, 'io_strategy'):
            self.io_strategy = ConsoleIO()

    def process_form_data(self, form_data):
        errors = []
        name = form_data.get('name', '').strip()
        cuisine = form_data.get('cuisine', '').strip()
        calories = form_data.get('calories', '').strip()

        if name:
            self.name = name
        else:
            errors.append("Название блюда обязательно")

        if cuisine:
            self.cuisine = cuisine
        else:
            errors.append("Кухня обязательна")

        if calories:
            try:
                self.calories = int(calories)
                if not (0 <= self.calories <= 3000):
                    errors.append("Калории должны быть в диапазоне 0-3000")
            except ValueError:
                errors.append("Калории должны быть числом")
        else:
            errors.append("Калории обязательны")

        return errors

    def prepare_for_display(self, index=None):
        dish_data = {
            'name': self.name,
            'cuisine': self.cuisine,
            'calories': self.calories,
            'type': self.__class__.__name__,
            'index': index
        }
        return dish_data

    # консоль
    def input(self):
        for field in self.field_labels:
            while True:
                value = self.io_strategy.input(self, field)
                if self._validate(field, value):
                    self._set_field(field, value)
                    break
                else:
                    print(f"Некорректное значение для '{self.field_labels[field]}'. Попробуйте снова.")

    def output(self):
        for field in self.field_labels:
            self.io_strategy.output(self, field)

    def edit(self):
        print(f"\nРедактирование {self.__class__.__name__}:")
        for field, label in self.field_labels.items():
            current = getattr(self, field)
            while True:
                new_value = self.io_strategy.input(
                    self,
                    f"{label} (текущее: {current}, Enter — оставить без изменений)"
                )
                if not new_value.strip():
                    break
                if self._validate(field, new_value):
                    self._set_field(field, new_value)
                    break
                else:
                    print(f"Некорректное значение для '{label}'. Попробуйте снова.")

    def _validate(self, field, value):
        if field in ["name", "cuisine"]:
            return bool(value.strip())
        if field == "calories":
            try:
                val = int(value)
                return 0 <= val <= 3000
            except ValueError:
                return False
        return True

    def _set_field(self, field, value):
        if field == "calories":
            value = int(value)
        setattr(self, field, value)


class MainDish(Dish):
    field_labels = Dish.field_labels | {"garnish": "Гарнир"}

    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.garnish = ""

    def process_form_data(self, form_data):
        errors = super().process_form_data(form_data)

        garnish = form_data.get('garnish', '').strip()
        if garnish:
            self.garnish = garnish
        else:
            errors.append("Гарнир обязателен для основного блюда")

        return errors

    def prepare_for_display(self, index=None):
        dish_data = super().prepare_for_display(index)
        dish_data['garnish'] = self.garnish
        return dish_data

    def _validate(self, field, value):
        if field == "garnish":
            return bool(value.strip())
        return super()._validate(field, value)


class Dessert(Dish):
    field_labels = Dish.field_labels | {"sweetness": "Сладость (1-10)"}

    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.sweetness = 5

    def process_form_data(self, form_data):
        errors = super().process_form_data(form_data)

        sweetness = form_data.get('sweetness', '').strip()
        if sweetness:
            try:
                self.sweetness = int(sweetness)
                if not (1 <= self.sweetness <= 10):
                    errors.append("Сладость должна быть в диапазоне 1-10")
            except ValueError:
                errors.append("Сладость должна быть числом")
        else:
            errors.append("Сладость обязательна для десерта")

        return errors

    def prepare_for_display(self, index=None):
        dish_data = super().prepare_for_display(index)
        dish_data['sweetness'] = self.sweetness
        return dish_data

    def _validate(self, field, value):
        if field == "sweetness":
            try:
                val = int(value)
                return 1 <= val <= 10
            except ValueError:
                return False
        return super()._validate(field, value)

    def _set_field(self, field, value):
        if field == "sweetness":
            value = int(value)
        super()._set_field(field, value)