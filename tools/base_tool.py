from abc import ABC, abstractmethod


class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    def description(self):
        return "No description."

    @property
    def version(self):
        return "1.0"

    @property
    def category(self):
        return "General"

    @abstractmethod
    def run(self, *args, **kwargs):
        pass