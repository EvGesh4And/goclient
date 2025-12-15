# app/asm2504/st06/equipment.py
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class Equipment:
    manufacturer: str = ""
    model: str = ""
    price: float = 0.0
    weight: float = 0.0

    io: Any = field(default=None, repr=False, compare=False)

    FIELD_DEFS = (
        ("manufacturer", "Производитель", ""),
        ("model", "Модель", ""),
        ("price", "Цена", 0.0),
        ("weight", "Вес (грамм)", 0.0),
    )

    def set_io(self, io):
        self.io = io

    def get_field_defs(self):
        return self.FIELD_DEFS

    def input_fields(self):
        if not self.io:
            raise RuntimeError("IO-стратегия не установлена для объекта.")
        for name, prompt, default in self.get_field_defs():
            current = getattr(self, name, default)
            value = self.io.input_field(self, name, prompt, current)
            setattr(self, name, value)

    def output_fields(self):
        if not self.io:
            raise RuntimeError("IO-стратегия не установлена для объекта.")
        print(f"--- {self.__class__.__name__} ---")
        for name, prompt, _ in self.get_field_defs():
            self.io.output_field(self, name, prompt)

    def __getstate__(self):
        st = self.__dict__.copy()
        st.pop("io", None)
        return st

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.io = None

    def to_row(self) -> Dict[str, object]:
        return {
            "manufacturer": self.manufacturer,
            "model": self.model,
            "price": self.price,
            "weight": self.weight,
        }

    @classmethod
    def from_row(cls, row: Dict[str, object]):
        obj = cls()
        obj.manufacturer = row.get("manufacturer", "")
        obj.model = row.get("model", "")
        obj.price = row.get("price", 0.0)
        obj.weight = row.get("weight", 0.0)
        return obj

    @staticmethod
    def detect_type(row: Dict[str, object]) -> str:
        t = row.get("type")
        if t:
            return t
        if row.get("focal_length") or row.get("max_aperture") or row.get("min_aperture"):
            return "lens"
        return "camera"

    def summary(self) -> str:
        return f"{self.manufacturer} {self.model}"
