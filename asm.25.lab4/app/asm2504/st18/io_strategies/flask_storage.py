import os
import pickle

class FlaskStorage:
    def __init__(self, filename="data.pkl"):
        self.filename = filename
        self.objects = self.load()

    def set_filename(self, filename):
        self.filename = filename
        self.objects = self.load()

    def get_filename(self):
        return self.filename

    def get_available_files(self, folder="."):
        pkl_files = [f for f in os.listdir(folder) if f.endswith(".pkl")]
        return pkl_files

    def add(self, obj):
        self.objects.append(obj)
        self.save()

    def get_all(self):
        return self.objects

    def get(self, idx):
        return self.objects[idx]

    def update(self, idx, obj):
        self.objects[idx] = obj
        self.save()

    def delete(self, idx):
        del self.objects[idx]
        self.save()

    def clear(self):
        self.objects = []
        self.save()

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.objects, f)

    def load(self):
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []