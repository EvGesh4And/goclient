import re
from typing import Any, Tuple

from .student import Student

class Headman(Student):
    """Староста"""
    def __init__(self, io = None):
        super().__init__(io)
        self.meetingsHeld: int | None = None
        self.electronicJournal: bool | None = None

    def input_fields(self):
        super().input_fields()
        # self.meetingsHeld = self.io.input_number("Enter number of meetings held: ", int, 0)
        # self.electronicJournal = self.io.input_string_regex("Enter access to electronic journal (y/n): ", r'\b[yYnN]\b', "Invalid input. Please try again: ") in ["y", "Y"]

        self.io.input_field(self, "meetingsHeld")
        self.io.input_field(self, "electronicJournal")

    def edit_fields(self):
        super().edit_fields()
        # meetingsHeld = self.io.input_number(f"Number of meetings held [{self.MeetingsHeld}]: ", int, 0, ignore_empty=True)
        # electronicJournal = self.io.input_string_regex("Enter access to electronic journal (y/n): ", r'^[yYnN]?$', "Invalid input. Please try again: ")
        # if meetingsHeld: self.MeetingsHeld = meetingsHeld
        # if electronicJournal: self.electronicJournal = electronicJournal in ["y", "Y"]

        self.io.input_field(self, "meetingsHeld")
        self.io.input_field(self, "electronicJournal")

    def output_fields(self):
        super().output_fields()
        # self.io.output(f"Meetings held: {self.MeetingsHeld}")
        # self.io.output(f"Electronic journal: {self.electronicJournal}")
        self.io.output_field(self, "meetingsHeld")
        self.io.output_field(self, "electronicJournal")

    def validate_field(self, field_name: str, raw: str) -> Tuple[bool, Any]:
        if field_name == "meetingsHeld":
            try:
                value = int(raw)
                if 0 <= value:
                    return True, value
                else:
                    return False, "Meetings held should be greater than 0"
            except ValueError:
                return False, "Meetings held should be an integer"
        if field_name == "electronicJournal":
            if not isinstance(raw, str):
                return False, "Value should be a string"
            pattern = r"^[yYnN]$"
            if re.match(pattern, raw):
                return True, raw in ["y", "Y"]
            return False, "Value should be 'y' or 'n'."
        return super().validate_field(field_name, raw)