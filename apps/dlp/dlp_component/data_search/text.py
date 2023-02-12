from abc import abstractmethod, ABCMeta


class BaseTextDataSearch(metaclass=ABCMeta):
    def __init__(self, text: str | None):
        self.text = text

    @abstractmethod
    def find_data(self, *args, **kwargs):
        raise NotImplementedError()
