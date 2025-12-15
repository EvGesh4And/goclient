from .asset import Asset


class Stock(Asset):
    def __init__(self, dividend_yield=0.0):
        super().__init__()
        self.dividend_yield = dividend_yield  # в процентах

    def input(self):
        super().input()
        if self.io_handler:
            self.dividend_yield = self.io_handler.input_float("Дивидендная доходность (%)")

    def output(self):
        super().output()
        if self.io_handler:
            self.io_handler.output("Дивидендная доходность", f"{self.dividend_yield:.2f}%")

    def get_type(self):
        return "Акция"