class ConsoleIO:
    def input_field(self, prompt):
        """Ввод поля из консоли."""
        return input(prompt)

    def output_field(self, field_name, value):
        """Вывод поля в консоль."""
        print(f"{field_name}: {value}")

    def output_entity(self, entity):
        """Вывод полной карточки сотрудника."""
        print("\n=== Карточка сотрудника ===")
        entity.output_fields()

    def display_list(self, entities):
        """Вывод списка сотрудников."""
        if not entities:
            print("Список сотрудников пуст.")
            return
        for i, ent in enumerate(entities, 1):
            print(f"\n--- Сотрудник {i} ---")
            self.output_entity(ent)
