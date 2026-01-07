from abc import ABC, abstractmethod
from pathlib import Path


class Agent(ABC):  # pragma: no cover
    """Defines the interfaces for any agent class"""

    @abstractmethod
    def select_action(
        self, state: str, valid_moves: list[tuple[int, int]]
    ) -> tuple[int, int]:
        """
        Choose an action given the current state and available actions.
        """
        pass

    @abstractmethod
    def update(
        self,
        start_state: str,
        action: tuple[int, int],
        reward: float,
        new_state: str,
        done: bool = False,
    ):
        """
        Update the agent's internal state based on an observed transition.
        """
        pass

    @abstractmethod
    def save(self, fp: Path):
        """
        Persist the agent's learned parameters to disk.
        """
        pass

    @abstractmethod
    def load(self, fp: Path):
        """
        Load previously saved parameters from disk.
        """
        pass
