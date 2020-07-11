from abc import ABC, abstractmethod


class AbstractBaseRepo(ABC):
    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def get(self, id_):
        pass

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def remove(self, item):
        pass
