from abc import ABC, abstractmethod

try:
    from .console_io import ConsoleIO
except ImportError:
    from console_io import ConsoleIO


class FinancialInstrument(ABC):
    """Абстрактный базовый класс для финансовых инструментов"""

    def __init__(self, name="", price=0.0, currency="USD", io_strategy=None):
        self.name = name
        self.price = price
        self.currency = currency
        self.io_strategy = io_strategy or ConsoleIO()

    @abstractmethod
    def input(self):
        pass

    @abstractmethod
    def output(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}, цена: {self.price} {self.currency}"


class Stock(FinancialInstrument):
    """Класс Акции"""

    def __init__(self, name="", price=0.0, currency="USD", dividend_yield=0.0, io_strategy=None):
        super().__init__(name, price, currency, io_strategy)
        self.dividend_yield = dividend_yield

    def input(self):
        self.name = self.io_strategy.input_string("Введите название акции")
        self.price = self.io_strategy.input_float("Введите текущую цену акции")
        self.currency = self.io_strategy.input_string("Введите валюту")
        self.dividend_yield = self.io_strategy.input_float("Введите дивидендную доходность (%)")

    def output(self):
        self.io_strategy.output("Тип", "Акция")
        self.io_strategy.output("Название", self.name)
        self.io_strategy.output("Цена", f"{self.price} {self.currency}")
        self.io_strategy.output("Дивидендная доходность", f"{self.dividend_yield}%")


class Bond(FinancialInstrument):
    """Класс Облигации"""

    def __init__(self, name="", price=0.0, currency="USD", coupon_rate=0.0,
                 maturity_years=1, face_value=1000.0, io_strategy=None):
        super().__init__(name, price, currency, io_strategy)
        self.coupon_rate = coupon_rate
        self.maturity_years = maturity_years
        self.face_value = face_value

    def input(self):
        self.name = self.io_strategy.input_string("Введите название облигации")
        self.price = self.io_strategy.input_float("Введите текущую цену")
        self.currency = self.io_strategy.input_string("Введите валюту")
        self.coupon_rate = self.io_strategy.input_float("Введите купонную ставку (%)")
        self.maturity_years = self.io_strategy.input_number("Введите срок до погашения (лет)")
        self.face_value = self.io_strategy.input_float("Введите номинальную стоимость")

    def output(self):
        self.io_strategy.output("Тип", "Облигация")
        self.io_strategy.output("Название", self.name)
        self.io_strategy.output("Цена", f"{self.price} {self.currency}")
        self.io_strategy.output("Купонная ставка", f"{self.coupon_rate}%")
        self.io_strategy.output("Срок до погашения", f"{self.maturity_years} лет")
        self.io_strategy.output("Номинальная стоимость", f"{self.face_value} {self.currency}")