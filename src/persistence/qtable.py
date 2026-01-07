"""
A class to manage a Q Table. States are represented by the string of the flattened
matrix for the tic-tac-toe table, with pieces represented by "X", "O" or "-", e.g.
one hame state might be "X-X-O-O--", and the corresponding board would look like
this:
    X| |X
    -----
     |O|
    -----
    O| |
Similarly, the available actions are represented by the string with numerical
indices of the column and row. E.g. "11" is the centre of the board, "10" is the
middle of the top row, etc.

Actions are float values.
"""

import csv
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from src.persistence import Persistence

default = {
    "00": 0.0,
    "01": 0.0,
    "02": 0.0,
    "10": 0.0,
    "11": 0.0,
    "12": 0.0,
    "20": 0.0,
    "21": 0.0,
    "22": 0.0,
}


class QTable(Persistence):
    def __init__(self) -> None:
        self.table: dict[str, dict[str, float]] = OrderedDict()

    def update(self, state: str, action: str, value: float) -> None:
        """Update the value of an action for a given state"""
        row = self.table.get(state, deepcopy(default))
        row[action] = value
        self.table[state] = row

    def get_values(self, state: str, action: None | str = None) -> dict[str, float]:
        """Get the value of a particular action in a particular state. If no
        action is provided, return the values of all actions."""
        all_state_values = self.table.get(state, deepcopy(default))
        if action is None:
            return default | all_state_values
        else:
            val = all_state_values.get(action, 0.0)
            return {action: val}

    def save(self, fp: Path) -> None:
        """Save Q-Table to file for later use"""
        with Path(fp).open("w") as csvfile:
            fieldnames = ["state", "00", "01", "02", "10", "11", "12", "20", "21", "22"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for state, actions in self.table.items():
                row = {"state": state} | actions
                writer.writerow(row)

    def load(self, fp: Path) -> None:
        """Load a Q-Table from a file"""
        with Path(fp).open(newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            self.table = OrderedDict()
            for row in reader:
                state = row.pop("state")
                self.table[state] = {k: float(v) if v else 0.0 for k, v in row.items()}
