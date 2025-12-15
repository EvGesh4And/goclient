from dataclasses import dataclass
from typing import Any, Dict
try:
    from .equipment import Equipment
except Exception:
    from equipment import Equipment

@dataclass
class Lens(Equipment):
    focal_length: str = ""
    max_aperture: str = ""
    min_aperture: str = ""
    bayonet: str = ""

    FIELD_DEFS = Equipment.FIELD_DEFS + (
        ("focal_length", "Фокусное расстояние", ""),
        ("max_aperture", "Макс. диафрагма", ""),
        ("min_aperture", "Мин. диафрагма", ""),
        ("bayonet", "Байонет (mount)", ""),
    )

    def get_field_defs(self):
        return self.FIELD_DEFS

    def to_row(self) -> Dict[str, object]:
        row = super().to_row()
        row.update({
            "type": "lens",
            "bayonet": self.bayonet,
            "focal_length": self.focal_length,
            "max_aperture": self.max_aperture,
            "min_aperture": self.min_aperture,
            "sensor_size": None,
            "megapixels": None,
        })
        return row

    @classmethod
    def from_row(cls, row: Dict[str, object]):
        obj = super(Lens, cls).from_row(row)
        obj.bayonet = row.get("bayonet", "")
        obj.focal_length = row.get("focal_length", "")
        obj.max_aperture = row.get("max_aperture", "")
        obj.min_aperture = row.get("min_aperture", "")
        return obj

    def summary(self) -> str:
        return f"{self.manufacturer} {self.focal_length}"
