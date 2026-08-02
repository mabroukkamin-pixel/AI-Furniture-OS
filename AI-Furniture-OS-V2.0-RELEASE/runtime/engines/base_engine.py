from abc import ABC, abstractmethod


class BaseEngine(ABC):

    def __init__(self, state=None):
        self.state = state

    @abstractmethod
    def generate(self, request):
        pass