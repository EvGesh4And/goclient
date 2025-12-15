import pickle

class PickleStorage:
    def read_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return []
    
    def write_to_file(self, data, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(data, file)
            return True
        except Exception as e:
            print(f"Ошибка записи файла: {e}")
            return False