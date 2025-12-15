import os
import pickle

bin_path = 'data/asm2504/st05/pickle/'

class PickleStorage:
    def __init__(self, name):
        try:
            self.load()
        except:
            self.items = {}
            self.maxid = 0

    def load(self):
        if not os.path.exists(bin_path):
            os.mkdir(bin_path)
        with open(bin_path + 'group.db', 'rb') as f:
            (self.maxid, self.items) = pickle.load(f)

    def store(self):
        with open(bin_path + 'group.db', 'wb') as f:
            pickle.dump((self.maxid, self.items), f)

    def get_item(self, id):
        if id in self.items:
            return self.items[id]
        else:
            return None

    def add(self, item):
        if item.id <= 0:
            self.maxid += 1
            item.id = self.maxid
            self.items[self.maxid] = item
        elif item.id in self.items:
            self.items[item.id] = item

    def edit(self, item):
        if item.id in self.items:
            self.items[item.id] = item

    def delete(self, id):
        if id in self.items:
            del self.items[id]

    def get_items(self):
        for (id, item) in self.items.items():
            yield item

    def size(self):
        return len(self.items)

    def clear(self):
        self.items = {}
