from abc import ABC, abstractmethod


class _GameString(ABC):

    @abstractmethod
    def str(self) -> str:
        """Return the object string representation of the game string."""
        pass

    def game_str(self) -> str:
        """Return the game string representation of the game string."""
        return f"/{self.str()}"

    def __eq__(self, other):
        return self.str() == str(other)

    def __str__(self):
        return self.str()
