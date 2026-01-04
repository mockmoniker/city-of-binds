from abc import ABC, abstractmethod


class _StringThing(ABC):
    @abstractmethod
    def str(self) -> str:
        """Return the object's string representation."""
        pass

    def __eq__(self, other):
        return self.str() == str(other)

    def __str__(self):
        return self.str()
