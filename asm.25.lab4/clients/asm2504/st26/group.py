from .storage_strategy import StorageStrategy, PickleStorage
from .io_strategy import IOStrategy, ConsoleIO
from .student import Student
from .headman import Headman
from .steward  import Steward


class Group:
    def __init__(self, storage: StorageStrategy = None, io: IOStrategy = None):
        self.students: dict[int, Student] = dict()
        self.io: IOStrategy = io if io else ConsoleIO()
        self.storage: StorageStrategy = storage if storage else PickleStorage()

    def show_all(self):
        self.io.output(f"~~~~~~~~~~START GROUP ~~~~~~~~~~")
        if not self.students:
            self.io.output("No students")
        else:
            for student in self.students.values():
                student.output_fields()
        self.io.output("~~~~~~~~~~~ END GROUP ~~~~~~~~~~~")

    def add(self):
        types = {
            1: ("Student", Student),
            2: ("Headman", Headman),
            3: ("Steward", Steward),
            0: ("Canceled", None),
        }

        for key, value in types.items():
            self.io.output(f"{key}. {value[0]}")
        choice = self.io.input_number("Select type: ", int, 0, 3)
        if choice == 0:
            self.io.output("Cancelled.")
            return

        cls = types[choice][1]
        item = cls(self.io)
        item.input_fields()
        self.students[item.id] = item
        self.io.output(f"Added: {item}")

    def edit(self):
        if not self.students:
            self.io.output("No students to edit")
            return
        self.show_all()
        _id = self.io.input_number("Enter ID to edit or 0 to cancel: ", int, 0, max(self.students.keys()))
        if _id == 0:
            self.io.output("Cancelled")
            return
        if _id not in list(self.students.keys()):
            self.io.output("Cancelled. Invalid ID")
            return
        self.students[_id].edit_fields()
        # raise NotImplementedError

    def delete(self):
        if not self.students:
            self.io.output("No students to delete")
            return
        self.show_all()
        _id = self.io.input_number("Enter ID to delete or 0 to cancel: ", int, 0, max(self.students.keys()))
        if _id == 0:
            self.io.output("Cancelled")
            return
        if _id not in list(self.students.keys()):
            self.io.output("Cancelled. Invalid ID")
            return
        try :
            del self.students[_id]
            self.io.output(f"Deleted: {_id}")
        except Exception as ex:
            # raise ex
            self.io.output(f"Error: {ex}")
            return

    def clear(self):
        if self.io.input_string_regex("Are you sure? (y/n): ", r'\b[yYnN]\b', "Invalid input. Please try again: ") in ["y", "Y"]:
            self.io.output("Cancelled")
            return
        self.students.clear()
        Student.reset_max_id()
        self.io.output("Group cleared")

    def save(self):
        if not self.students:
            self.io.output("No students")
            return
        self.storage.save(self.students)

    def load(self):
        if self.students:
            if self.io.input_string_regex("Group not empty. When loading, the previous data will be lost! Are you sure? (y/n): ", r'\b[yYnN]\b', "Invalid input. Please try again: ") in ["y", "Y"]:
                self.students.clear()
                Student.reset_max_id()
            else:
                self.io.output("Cancelled")
                return
        self.students = self.storage.load()