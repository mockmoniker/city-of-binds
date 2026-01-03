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


class _GenericGameString(_StringThing):

    @abstractmethod
    def game_str(self) -> str:
        """Return the game string representation of the object."""
        pass


class _CommandString(_GenericGameString):
    def game_str(self) -> str:
        """
        Return the game string representation that would be used to run this command in-game.

        The game string is the exact format required by City of Heroes to execute
        the command, including any necessary prefixes, formatting, or syntax.

        Returns:
            str: The command string as it would appear when executed in the game client.
        """
        return f"/{self.str()}"
