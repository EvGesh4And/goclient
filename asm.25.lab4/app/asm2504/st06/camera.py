from dataclasses import dataclass
from typing import Dict
try:
    from .equipment import Equipment
except Exception:
    from equipment import Equipment

@dataclass
class Camera(Equipment):
    sensor_size: str = ""
    megapixels: float = 0.0
    bayonet: str = ""

    FIELD_DEFS = Equipment.FIELD_DEFS + (
        ("sensor_size", "Размер матрицы", ""),
        ("megapixels", "Разрешение (МП)", 0.0),
        ("bayonet", "Байонет (mount)", ""),
    )

    def get_field_defs(self):
        return self.FIELD_DEFS

    def to_row(self) -> Dict[str, object]:
        row = super().to_row()
        row.update({
            "type": "camera",
            "bayonet": self.bayonet,
            "sensor_size": self.sensor_size,
            "megapixels": self.megapixels,
            "focal_length": None,
            "max_aperture": None,
            "min_aperture": None,
        })
        return row

    @classmethod
    def from_row(cls, row: Dict[str, object]):
        obj = super(Camera, cls).from_row(row)
        obj.bayonet = row.get("bayonet", "")
        obj.sensor_size = row.get("sensor_size", "")
        obj.megapixels = row.get("megapixels", 0.0)
        return obj

    def summary(self) -> str:
        return f"{self.manufacturer} {self.megapixels}MP"
