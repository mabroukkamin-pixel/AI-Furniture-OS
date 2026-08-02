from abc import ABC, abstractmethod


class BaseClient(ABC):

    @abstractmethod
    def generate(self, prompt, image_path):
        pass