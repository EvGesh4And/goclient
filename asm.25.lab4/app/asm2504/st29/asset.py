from abc import ABC, abstractmethod


class Asset(ABC):
    def __init__(self, name="", price=0.0, currency="USD"):
        self.name = name
        self.price = price
        self.currency = currency
        self.io_handler = None
        self.id = None

    def set_io_handler(self, io_handler):
        self.io_handler = io_handler

    def input(self):
        if self.io_handler:
            self.name = self.io_handler.input_string("Название актива")
            self.price = self.io_handler.input_float("Цена")
            self.currency = self.io_handler.input_string("Валюта")

    def output(self):
        if self.io_handler:
            self.io_handler.output("Название", self.name)
            self.io_handler.output("Цена", f"{self.price:.2f}")
            self.io_handler.output("Валюта", self.currency)

    @abstractmethod
    def get_type(self):
        pass