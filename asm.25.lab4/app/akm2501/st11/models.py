from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Sequence


FIELD_LABELS = {
    "species": "Вид",
    "habitat": "Среда обитания",
    "behavior": "Поведение",
    "hunting_style": "Стиль охоты",
    "favorite_plant": "Любимое растение",
    "time": "Обновлено",
}


@dataclass
class Animal:
    id: str | None = None
    species: str = ""
    habitat: str = ""
    behavior: str = ""
    time: datetime | None = None
    io = None

    @classmethod
    def fields(cls) -> Sequence[str]:
        return ("species", "habitat", "behavior")

    def input_data(self, io) -> None:
        self.io = io
        for field in self.fields():
            setattr(self, field, io.input_field(self, field))
        self.time = datetime.now()

    def output_data(self) -> Dict[str, str]:
        data: Dict[str, str] = {}
        if self.io:
            for field in self.fields():
                label = FIELD_LABELS.get(field, field)
                data[label] = getattr(self, field, "")
        return data

    def __str__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"Species: {self.species}\n"
            f"Habitat: {self.habitat}\n"
            f"Behavior: {self.behavior}\n"
            f"Time: {self.time}"
        )


@dataclass
class Predator(Animal):
    hunting_style: str = ""

    @classmethod
    def fields(cls) -> Sequence[str]:
        base = list(super().fields())
        base.append("hunting_style")
        return base

    def input_data(self, io) -> None:
        super().input_data(io)
        self.hunting_style = io.input_field(self, "hunting_style")

    def output_data(self) -> Dict[str, str]:
        data = super().output_data()
        if self.io:
            label = FIELD_LABELS.get("hunting_style", "hunting_style")
            data[label] = getattr(self, "hunting_style", "")
        return data


@dataclass
class Herbivore(Animal):
    favorite_plant: str = ""

    @classmethod
    def fields(cls) -> Sequence[str]:
        base = list(super().fields())
        base.append("favorite_plant")
        return base

    def input_data(self, io) -> None:
        super().input_data(io)
        self.favorite_plant = io.input_field(self, "favorite_plant")

    def output_data(self) -> Dict[str, str]:
        data = super().output_data()
        if self.io:
            label = FIELD_LABELS.get("favorite_plant", "favorite_plant")
            data[label] = getattr(self, "favorite_plant", "")
        return data