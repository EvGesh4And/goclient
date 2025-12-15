import pickle
import os
# from console_io import ConsoleIO

class PickleStorage:
    def __init__(self, filename="cardex.pkl"):
        # place student data under project `data/<group>/<student>/` for consistency
        current_dir = os.path.dirname(os.path.abspath(__file__))
        student_folder = os.path.basename(current_dir)
        group_folder = os.path.basename(os.path.dirname(current_dir))
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        target_dir = os.path.join(project_root, 'data', group_folder, student_folder)
        os.makedirs(target_dir, exist_ok=True)
        self.filename = os.path.join(target_dir, filename)

    def save(self, entities):
        """Save list of entities to a pickle file (stores dicts produced by `to_dict`)."""
        if not entities:
            print("Список пуст. Нечего сохранять.")
            return
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump([ent.to_dict() for ent in entities], f)
            print(f"Сохранено в {self.filename}")
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")

    def load(self, entity_class_from_dict):
        """Load list of entities from pickle and reconstruct objects using provided factory."""
        if not os.path.exists(self.filename):
            # no file yet → return empty list
            return []
        try:
            with open(self.filename, 'rb') as f:
                data_list = pickle.load(f)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

        entities = []
        for data in data_list:
            try:
                entities.append(entity_class_from_dict(data))
            except Exception as e:
                print(f"Ошибка при восстановлении записи: {e}")
        return entities