from abc import ABC, abstractmethod

class IOHandler(ABC):
    @abstractmethod
    def read(self, field):
        pass

    @abstractmethod
    def write(self, title, value):
        pass

    def info(self, message):
        pass