from clients.akm2501.st18.card_index import CardIndex
from app.akm2501.st18.io.console import ConsoleIO
from clients.akm2501.st18.menu import Menu
from app.akm2501.st18.storage.rest import RestStorage


def main() -> None:
    io = ConsoleIO()
    storage = RestStorage()
    card_index = CardIndex(storage, io)
    menu = Menu(card_index)
    menu.run()
