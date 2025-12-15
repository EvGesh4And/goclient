from flask import jsonify

from ..io_handlers.io_handler import IOHandler


class RESTIOHandler(IOHandler):
    def __init__(self, io):
        self.io = io

    def read(self, field):
        return self.io.json.get(field, None)

    def write(self, title, value):
        print(value)

    def info(self, message):
        return jsonify({'info': message})

    def get_output(self):
        return "".join(self.output)
