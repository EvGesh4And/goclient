import pickle
import os
from .storage import add_entity


LR1_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "asm2504", "st01", "cardex.pkl")


def import_from_lr1():
    if not os.path.exists(LR1_PATH):
        return 0

    try:
        with open(LR1_PATH, "rb") as f:
            entities = pickle.load(f)
            # print(entities)
        imported_count = 0
        for ent in entities:
            try:
                data = {
                    "type": ent['type'].lower(),
                    "name": ent['name'],
                    "age": ent['age'],
                    "group_role": ent.get("group_role")
                }
                add_entity(data)
                imported_count += 1
            except ValueError as e:
                print(e)
                continue

        # print(f"Imported {imported_count} lr1")
        return imported_count
    except Exception as e:
        # print(f"Error import from lr1: {e}")
        return 0
