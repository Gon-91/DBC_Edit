from abc import ABC, abstractmethod

class Usecase(ABC):
    @abstractmethod
    def execute(self):
        pass
    def can_execute(self) -> bool :
        return True