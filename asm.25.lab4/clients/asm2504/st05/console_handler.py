from .io_handler import IOHandler

class ConsoleIOHandler(IOHandler):
    def read(self, field):
        return input(f"Введите {field}: ")

    def write(self, title, value):
        print(f"{title}: {value}")

    def info(self, message):
        print(f"info: {message}")
