if __name__ == '__main__':
    from employee import Employee
    from director import Director
    from manager import Manager
    from strategy_io import Console_IO
else:
    from .employee import Employee
    from .director import Director
    from .manager import Manager
    from .strategy_io import Console_IO


class Company:
    def __init__(self, storage):
        self.io = Console_IO()
        self.storage = storage

    def add_element(self):
        print('\nChoose an option:\n 1. Employee\n 2. Manager\n 3. Director\n')
        request = int(input('Type your request (1-3) = '))

        match request:
            case 1:
                emp = Employee(self.io)
            case 2:
                emp = Manager(self.io)
            case 3:
                emp = Director(self.io)
            case _:
                print('Request should be a number in range 1-3. Try again')
                return

        print()

        emp.set_data()

        if self.storage.add_employee(emp):
            print(f"\nEmployee was successfully added (ID: {emp.id})")
        else:
            print("Error occurred while adding employee")

    def print_elements(self):
        employees = self.storage.get_employees()

        if not employees:
            print('There are no employees')
            return

        for i, emp in enumerate(employees, 1):
            emp.io = self.io
            print(f"\n{i}. {emp.__class__.__name__}")
            emp.get_data()

    def edit_element(self):
        employees = self.storage.get_employees()

        if not employees:
            print('There are no employees to edit')
            return

        for i, p in enumerate(employees, 1):
            print(f"{i}. {p.name} ({p.__class__.__name__})")

        try:
            idx = int(input('\nChoose an employee to edit = ')) - 1
            if 0 <= idx < len(employees):
                emp = employees[idx]
                emp.io = self.io

                print(f'\nChoose a field to edit, 0 - change all fields')
                fields = emp.get_editable_fields()

                for i, field in enumerate(fields, 1):
                    print(f"{i}. {field}")

                request = int(input("\nChoose an option = "))
                if request == 0:
                    emp.set_data()
                elif 1 <= request <= len(fields):
                    field_name = fields[request - 1]
                    new_value = input(f"\nEnter new {field_name}: ")
                    current_val = getattr(emp, field_name)
                    if isinstance(current_val, int):
                        try:
                            new_value = int(new_value)
                        except ValueError:
                            print("Wrong option was chosen. Try again")
                            return
                    setattr(emp, field_name, new_value)
                else:
                    print("Invalid field number.")
                    return
                if self.storage.update_employee(emp):
                    print("Employee was successfully updated")
                else:
                    print("Update failed.")
            else:
                print("Invalid employee number")
        except ValueError:
            print("Enter a valid number")

    def delete_element(self):
        employees = self.storage.get_employees()

        if not employees:
            print('There is nothing to delete')
            return

        for i, p in enumerate(employees, 1):
            print(f"{i}. {p.name}")

        try:
            idx = int(input('\nChoose an employee to delete =  ')) - 1
            if 0 <= idx < len(employees):
                person = employees[idx]
                if self.storage.delete_employee(person.id):
                    print("Employee was successfully deleted from server")
                else:
                    print("Deletion failed")
            else:
                print("Invalid number")
        except ValueError:
            print("Enter a valid number")

    def delete_all_elements(self):
        if self.storage.delete_all_employees():
            print("All employees were deleted successfully")
        else:
            print("An error occurred while deleting")

    def save_elements(self):
        employees = self.storage.get_employees()
        self.storage.save_data(employees)

    def load_elements(self):
        self.storage.load_data()