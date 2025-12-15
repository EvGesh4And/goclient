import pickle
from pathlib import Path
from typing import Dict, Optional

from app.akm2501.st18.models import Item


class PickleStorage:
    def __init__(self):
        data_directory = Path(__file__).resolve().parents[3] / "data" / "akm2501" / "st18"
        data_directory.mkdir(parents=True, exist_ok=True)

        self.__data_file = data_directory / "data.pickle"

    def load(self):
        if not self.__data_file.exists():
            return 0, {}

        with open(self.__data_file, 'rb') as f:
            data = pickle.load(f)
            max_id = data.get('max_id', 0)
            items = data.get('items', {})
            return max_id, items

    def store(self, max_id: int, items: Dict[int, Item]):
        data = {
            'max_id': max_id,
            'items': items
        }
        with open(self.__data_file, 'wb') as f:
            pickle.dump(data, f)

    def get_items(self) -> Dict[int, Item]:
        _, items = self.load()
        return items

    def get(self, id: int) -> Optional[Item]:
        items = self.get_items()
        return items.get(id)

    def add(self, item: Item) -> int:
        max_id, items = self.load()
        new_id = max_id + 1
        item.id = new_id
        items[new_id] = item
        self.store(new_id, items)
        return new_id

    def update(self, item: Item) -> None:
        max_id, items = self.load()
        if item.id in items:
            items[item.id] = item
            self.store(max_id, items)

    def delete(self, id: int) -> bool:
        max_id, items = self.load()
        if id in items:
            del items[id]
            self.store(max_id, items)
            return True
        return False

    def clear(self) -> bool:
        self.store(0, {})
        return True
