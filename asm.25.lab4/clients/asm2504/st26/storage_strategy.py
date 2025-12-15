import pickle, os


class StorageStrategy:
    def __init__(self):
        pass

    def load(self, filename):
        raise NotImplementedError

    def save(self, data, filename):
        raise NotImplementedError


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PickleStorage(StorageStrategy):
    def __init__(self, filename = "storage"):
        super().__init__()
        self._filename = f"./asm2504/st26/{filename}.pkl"

    def load(self, filename = None):
        if filename is None:
            filename = self._filename

        if not os.path.exists(filename):
            print(f"File {filename} not found")
            return {}

        try:
            with open(filename, "rb") as file:
                data = pickle.load(file)
                print(f"Data loaded from {filename}")
                return data
        except Exception as ex:
            raise Exception(f"Error loading data: {ex}")

    def save(self, data, filename = None):
        if filename is None:
            filename = self._filename

        if os.path.exists(filename):
            print(f"File {filename} already exists")
            confirm = input("Type 'y' to overwrite the file or 'n' to cancel: ").strip()
            if confirm not in ["Y", "y", "Yes", "yes", "Д", "д", "Да", "да"]:
                print("Cancelled")
                return
            else:
                os.remove(filename)

        try:
            with open(filename, "wb") as file:
                pickle.dump(data, file)
        except Exception as ex:
            raise Exception(f"Error saving data: {ex}")
        print(f"Data saved to {filename}")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class APIStorage(StorageStrategy):
    def __init__(self, base_url = "localhost:5000/api/st26"):
        super().__init__()
        self._base_url = base_url

    def load(self, filename = None):
        if filename is None:
            filename = self._filename

        if not os.path.exists(filename):
            print(f"File {filename} not found")
            return {}

        try:
            with open(filename, "rb") as file:
                data = pickle.load(file)
                print(f"Data loaded from {filename}")
                return data
        except Exception as ex:
            raise Exception(f"Error loading data: {ex}")

    def save(self, data, filename = None):
        if filename is None:
            filename = self._filename

        if os.path.exists(filename):
            print(f"File {filename} already exists")
            confirm = input("Type 'y' to overwrite the file or 'n' to cancel: ").strip()
            if confirm not in ["Y", "y", "Yes", "yes", "Д", "д", "Да", "да"]:
                print("Cancelled")
                return
            else:
                os.remove(filename)

        try:
            with open(filename, "wb") as file:
                pickle.dump(data, file)
        except Exception as ex:
            raise Exception(f"Error saving data: {ex}")
        print(f"Data saved to {filename}")