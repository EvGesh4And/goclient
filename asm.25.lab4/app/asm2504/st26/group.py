from .storage_strategy import *
# from .io_strategy import *
from .student import *
from .headman import *
from .steward import *
import os
import pickle

class Group:
    def __init__(self, storage: StorageStrategy = None, io: IOStrategy = None):
        # self.students: dict[int, Student] = dict()
        self.io: IOStrategy = io if io else FlaskIO()
        self.storage: DBStorage = storage if storage else DBStorage()

    def get_all(self):
        return self.storage.get_items()

    def get_by_id(self, _id: int):
        return self.storage.get_item(_id)

    def add(self, type: str):
        types = {
            "Student": Student,
            "Headman": Headman,
            "Steward": Steward,
        }

        cls = types[type]
        item = cls(self.io)
        item.input_fields()
        self.storage.process_item(item)
        # self.io.output_message(f"Added: {type}, ID: {item.id}")

    def edit(self, _id: int):
        item = self.storage.get_item(_id)
        if item:
            item.edit_fields()
            self.storage.process_item(item)
            # self.io.output_message(f"Edited: {_id}")
        else:
            # self.io.output_message(f"Item not found: {_id}")
            pass

    def delete(self, _id: int):
        try :
            self.storage.delete_item(_id)
            # self.io.output_message(f"Deleted: {_id}")
        except Exception as ex:
            # self.io.output_message(f"Error: {ex}")
            return

    def clear(self):
        self.storage.clear_items()
        # self.io.output_message("Group cleared")

    def save(self):
        pkl_storage = PickleStorage()
        pkl_storage.save(self.get_all(), "group.pkl", True)
        # raise NotImplementedError

    def load(self):
        pkl_storage = PickleStorage()
        tmp = []
        try:
            tmp = pkl_storage.load()
        except Exception as ex:
            print(ex)
            # self.io.output_message(f"Error loading data: {ex}")
            pass
        if isinstance(tmp, dict):
            tmp = tmp.values()
        for item in tmp:
            item.io = self.io
            self.storage.process_item(item, True)
        # raise NotImplementedError