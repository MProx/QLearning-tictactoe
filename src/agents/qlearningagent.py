from pathlib import Path

from src.agents import Agent
from src.persistence import QTable


class QLearningAgent(Agent):
    def __init__(
        self,
        alpha: float = 0.2,
        gamma: float = 0.9,
    ) -> None:
        """
        marker (str): Player's mark ("X" or "O")
        alpha (float): Learning rate. Default 0.05.
        gamma (float): Discount factor for future rewards. Default 0.9.
        """
        self.qtable = QTable()
        self.alpha = alpha
        self.gamma = gamma

    def select_action(
        self, state: str, valid_moves: list[tuple[int, int]]
    ) -> tuple[int, int]:
        """Select the best move to play for a given state. Return the coordinates
        in (row, col) form"""
        if not valid_moves:
            raise RuntimeError("No valid moves")
        all_action_values = self.qtable.get_values(state)
        valid_moves_str = [f"{i}{j}" for i, j in valid_moves]
        valid_action_values: dict[str, float] = {
            k: v for k, v in all_action_values.items() if k in valid_moves_str
        }
        best_action = max(valid_action_values, key=lambda k: valid_action_values[k])
        return int(best_action[0]), int(best_action[1])

    def update(
        self,
        start_state: str,
        action: tuple[int, int],
        reward: float,
        new_state: str,
        done: bool = False,
    ) -> None:
        """Update the Q-Table based on the outcome of the action played

        Arguments:
        start_state (str): String representation of state before the move was played
        action (tuple[int, int]): Coordinates of move played (row, col)
        reward (float): Reward received (can be zero)
        new_state (str): String representation of state after the move was played
        done (bool): Set to True if the game is over
        """
        action_str = f"{action[0]}{action[1]}"
        q = self.qtable.get_values(start_state, action_str)[action_str]
        q_next_all = self.qtable.get_values(new_state)
        max_future_reward = 0.0 if done else max(q_next_all.values())
        q_next = (1 - self.alpha) * q + self.alpha * (
            reward + self.gamma * max_future_reward
        )
        self.qtable.update(start_state, action_str, q_next)

    def save(self, fp: Path):
        self.qtable.save(fp)

    def load(self, fp: Path):
        self.qtable.load(fp)
