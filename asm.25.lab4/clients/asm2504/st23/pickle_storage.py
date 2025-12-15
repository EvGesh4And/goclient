import pickle

class PickleStorage:
    def save(self, filename, data):
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def load(self, filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
