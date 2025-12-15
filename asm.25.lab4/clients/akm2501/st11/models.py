from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Sequence


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

    def print_fields(self) -> None:
        if self.io is None:
            return
        output = self.output_data()
        for name, value in output.items():
            print(f"{name}: {value}")

    def output_data(self) -> Dict[str, str]:
        result: Dict[str, str] = {}
        if self.io:
            for field in self.fields():
                self.io.output_field(self, field, result)
        return result


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
        result = super().output_data()
        if self.io:
            self.io.output_field(self, "hunting_style", result)
        return result


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
        result = super().output_data()
        if self.io:
            self.io.output_field(self, "favorite_plant", result)
        return result

