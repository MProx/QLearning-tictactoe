from abc import ABC, abstractmethod
from pathlib import Path


class Persistence(ABC):  # pragma: no cover
    """Defines the interface for any persistence class"""

    @abstractmethod
    def get_values(self, state: str, action: None | str = None) -> dict[str, float]:
        """Get the values of actions associated with a given state. If a specific action
        is provided, return that specific action in the value, otherwise return the
        value of all actions"""
        pass

    @abstractmethod
    def update(self, state: str, action: str, value: float) -> None:
        """Add a state, action and value to the agnet's persistent memory"""
        pass

    @abstractmethod
    def save(self, fp: Path):
        """The path to which to save the agent for later loading"""
        pass

    @abstractmethod
    def load(self, fp: Path):
        """The path from which to load the agent"""
        pass
