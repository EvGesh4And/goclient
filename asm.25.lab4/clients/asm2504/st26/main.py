if __name__ == '__main__':
    from group import Group
    from io_strategy import ConsoleIO
    from storage_strategy import PickleStorage
else:
    from .group import Group
    from .io_strategy import ConsoleIO
    from .storage_strategy import PickleStorage


def main():
    storage = PickleStorage()
    io = ConsoleIO()
    group = Group(storage, io)

    menu = {
        1: ("Show all", group.show_all),
        2: ("Add", group.add),
        3: ("Edit", group.edit),
        4: ("Delete", group.delete),
        5: ("Clear", group.clear),
        6: ("Save", group.save),
        7: ("Load", group.load),
        0: ("Exit", None)
    }

    while True:
        for key, (desc, _) in menu.items():
            io.output(f"{key}. {desc}")
        # choice = int(input("Select action: ").strip())
        choice = io.input_number("Select action: ", int, 0, 7)
        # if choice not in menu:
        #     io.output("Invalid choice")
        #     continue
        if choice == 0:
            io.output("Exiting")
            return
        try:
            action = menu[choice][1]
            action()
        except Exception as ex:
            print("Error:", ex)
        io.output("")


if __name__ == '__main__':
    main()
