class ConsoleIO:
    def input_field(self, prompt):
        """Ввод поля из консоли."""
        return input(prompt)

    def output_field(self, field_name, value):
        """Вывод поля в консоль."""
        print(f"{field_name}: {value}")

    def output_entity(self, entity):
        """Вывод всей карточки."""
        # Print a title similar to web UI: localized type name then fields
        type_name_map = {
            'Student': 'Студент',
            'Starosta': 'Староста'
        }
        ent_type = entity.__class__.__name__
        title = type_name_map.get(ent_type, ent_type)
        print(f"{title}")
        entity.output_fields()

    def display_list(self, entities):
        """Вывод картотеки."""
        if not entities:
            print("Список пуст.")
            return
        for ent in entities:
            id_str = getattr(ent, 'id', 'N/A')
            print(f"\n--- Карточка ID {id_str} ---")
            self.output_entity(ent)