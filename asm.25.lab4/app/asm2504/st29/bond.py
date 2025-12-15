from .asset import Asset


class Bond(Asset):
    def __init__(self, coupon_rate=0.0, maturity_years=1, face_value=1000):
        super().__init__()
        self.coupon_rate = coupon_rate  # в процентах
        self.maturity_years = maturity_years  # лет до погашения
        self.face_value = face_value  # номинальная стоимость

    def input(self):
        super().input()
        if self.io_handler:
            self.coupon_rate = self.io_handler.input_float("Купонная ставка (%)")
            self.maturity_years = self.io_handler.input_number("Срок до погашения (лет)")
            self.face_value = self.io_handler.input_float("Номинальная стоимость")

    def output(self):
        super().output()
        if self.io_handler:
            self.io_handler.output("Купонная ставка", f"{self.coupon_rate:.2f}%")
            self.io_handler.output("Срок до погашения", f"{self.maturity_years} лет")
            self.io_handler.output("Номинальная стоимость", f"{self.face_value:.2f}")

    def get_type(self):
        return "Облигация"