from abc import abstractmethod, ABC
class Generator(ABC):
    @abstractmethod
    def generate(self, query: str, context: str) -> str:
        pass