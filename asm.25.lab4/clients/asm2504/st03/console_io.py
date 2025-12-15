# Ввод/вывод в консоль
class ConsoleIO:
    def input_field(self, prompt):
        return input(prompt)

    def output_field(self, field_name, value):
        label_map = {
            "Тип": "Тип",
            "Название": "Название",
            "price": "Цена",
            "calories": "Калорийность",
            "ingredients": "Ингредиенты",
        }
        label = label_map.get(field_name, field_name)

        if field_name == "price" and isinstance(value, (int, float)):
            print(f"{label}: {value:.2f} ₽")
        elif field_name == "ingredients":
            if isinstance(value, list):
                print(f"{label}: {','.join(map(str, value)) if value else '-'}")
            else:
                print(f"{label}: {value}")
        else:
            print(f"{label}: {value}")

    def output_entity(self, entity):
        """Вывод всей карточки блюда."""
        entity.output_fields()

    def display_list(self, entities):
        """Вывод всего меню (по-русски)."""
        if not entities:
            print("Меню пусто.")
            return
        for i, ent in enumerate(entities, 1):
            print(f"\n--- Блюдо №{i} ---")
            self.output_entity(ent)
