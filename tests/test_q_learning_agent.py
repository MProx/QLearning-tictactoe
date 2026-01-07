import csv
from copy import deepcopy
from pathlib import Path

import pytest

from src.agents.qlearningagent import QLearningAgent


@pytest.fixture
def qlearningagent():
    return QLearningAgent("O")


def test_select_action(qlearningagent: QLearningAgent) -> None:
    """Test that the correct move is selected from the Q-table for a given state"""

    # Assign arbitrary values to a state:
    state = "----X----"
    values: dict[str, float] = {
        "00": 0.1,
        "01": 1.2,
        "02": 2.2,  # <- highest
        "10": 0.1,
        "12": 2.1,  # <- second highest
        "20": 0.0,
        "21": 1.2,
        "22": 2.0,
    }
    qlearningagent.qtable.table = {state: values}
    valid_moves_all = [(int(key[0]), int(key[1])) for key in values.keys()]
    row, col = qlearningagent.select_action(state, valid_moves=valid_moves_all)

    # Now try limiting valid moves:
    valid_moves_limited = [(1, 0), (2, 1), (1, 2)]
    row, col = qlearningagent.select_action(state, valid_moves=valid_moves_limited)
    assert (row, col) == (1, 2)


def test_select_action_none_available(qlearningagent: QLearningAgent) -> None:
    # Assign arbitrary values to a state:
    state = "----X----"
    values: dict[str, float] = {
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
    qlearningagent.qtable.table = {state: values}

    with pytest.raises(RuntimeError):
        qlearningagent.select_action(
            state,
            valid_moves=[],  # <- No valid moves
        )


def test_update_with_reward(qlearningagent: QLearningAgent) -> None:
    """Test that updates work as expected"""

    # Set up Q-Table
    qlearningagent.qtable.table = {
        "--X-O----": {
            "00": 0.0,
            "01": 0.0,
            "02": 0.0,
            "10": 0.0,
            "11": 0.0,
            "12": 0.0,
            "20": 0.0,
            "21": 0.0,
            "22": 0.0,
        },
        "X-X-O--O-": {
            "00": 0.0,
            "01": 100.0,
            "02": 0.0,
            "10": 0.0,
            "11": 0.0,
            "12": 0.0,
            "20": 0.0,
            "21": 0.0,
            "22": 0.0,
        },
    }

    # Set up qlearningagent:
    qlearningagent.alpha = 0.05
    qlearningagent.gamma = 0.95

    qlearningagent.update(
        start_state="--X-O----",
        action=(0, 0),
        reward=1,
        new_state="X-X-O--O-",
    )

    # Check everything except the updated value:
    expected_qtable = deepcopy(qlearningagent.qtable.table)
    updated_val = qlearningagent.qtable.table["--X-O----"].pop("00")
    del expected_qtable["--X-O----"]["00"]
    assert qlearningagent.qtable.table == expected_qtable

    # Check that value of (0, 0) action in Q-table was updated:
    assert updated_val == pytest.approx(4.8)


def test_save_checkpoint(qlearningagent: QLearningAgent, tmp_path: Path) -> None:
    """Test that the save method generates a CSV file of the correct
    formagt"""
    # Assign arbitrary values to a state:
    assert qlearningagent.qtable.table == {}
    qlearningagent.qtable.table["----X----"] = {"00": 0.1, "01": 1.2, "21": 1.2}
    qlearningagent.qtable.table["O---X----"] = {"12": 10.5, "02": 0.1}

    csvpath = tmp_path / "qlearningagent_O.csv"
    qlearningagent.save(csvpath)

    assert csvpath.exists()
    with Path(csvpath).open(newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        expected_header = [
            "state",
            "00",
            "01",
            "02",
            "10",
            "11",
            "12",
            "20",
            "21",
            "22",
        ]
        assert header == expected_header

        first_row = next(reader)
        assert first_row == ["----X----", "0.1", "1.2", "", "", "", "", "", "1.2", ""]

        second_row = next(reader)
        assert second_row == ["O---X----", "", "", "0.1", "", "", "10.5", "", "", ""]

        with pytest.raises(StopIteration):
            next(reader)  # Exception at end of file (no more rows)


def test_load_checkpoint(qlearningagent: QLearningAgent, tmp_path: Path) -> None:
    """Test taht a checkpoint file can be loaded into a Q-table"""

    # Create dummy checkpoint file with arbitrary data:
    header = [
        "state",
        "00",
        "01",
        "02",
        "10",
        "11",
        "12",
        "20",
        "21",
        "22",
    ]
    first_row = {"state": "----X----", "00": 0.1, "01": 1.2, "21": 1.2}
    second_row = {"state": "O---X----", "12": 10.5, "02": 0.1}
    csvpath = tmp_path / "qlearningagent_O.csv"
    with Path(csvpath).open("w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows([first_row, second_row])

    qlearningagent.load(csvpath)

    print(qlearningagent.qtable.table)
    assert qlearningagent.qtable.table == {
        "----X----": {
            "00": 0.1,
            "01": 1.2,
            "02": 0.0,
            "10": 0.0,
            "11": 0.0,
            "12": 0.0,
            "20": 0.0,
            "21": 1.2,
            "22": 0.0,
        },
        "O---X----": {
            "00": 0.0,
            "01": 0.0,
            "02": 0.1,
            "10": 0.0,
            "11": 0.0,
            "12": 10.5,
            "20": 0.0,
            "21": 0.0,
            "22": 0.0,
        },
    }
