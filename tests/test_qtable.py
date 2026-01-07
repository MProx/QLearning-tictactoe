import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest

from src.persistence.qtable import QTable


@pytest.fixture
def qtable():
    return QTable()


def test_update_new_entry(qtable: QTable):
    """Test that the update method adds new entries to the table"""
    # Check table is empty:
    assert qtable.table == {}

    # Add a new entry:
    qtable.update(state="----X----", action="10", value=100.0)
    assert qtable.table == {
        "----X----": {
            "00": 0.0,
            "01": 0.0,
            "02": 0.0,
            "10": 100.0,
            "11": 0.0,
            "12": 0.0,
            "20": 0.0,
            "21": 0.0,
            "22": 0.0,
        }
    }


def test_update_existing_entry(qtable: QTable):
    """Test that the update method updates existing entries to the table"""
    # Check table is empty:
    assert qtable.table == {}

    # Add a new entry:
    qtable.update(state="----X----", action="00", value=100.0)
    assert qtable.table == {
        "----X----": {
            "00": 100.0,
            "01": 0.0,
            "02": 0.0,
            "10": 0.0,
            "11": 0.0,
            "12": 0.0,
            "20": 0.0,
            "21": 0.0,
            "22": 0.0,
        }
    }

    # Update that same another:
    qtable.update(state="----X----", action="00", value=200.0)
    assert qtable.table == {
        "----X----": {
            "00": 200.0,  # <- updated value
            "01": 0.0,
            "02": 0.0,
            "10": 0.0,
            "11": 0.0,
            "12": 0.0,
            "20": 0.0,
            "21": 0.0,
            "22": 0.0,
        }
    }


def test_get_state_values(qtable: QTable):
    """Test that the value of an action in a state can be correctly retrieved"""
    qtable.table = {"----X----": {"01": 100.0}}  # Q-table is not empty
    assert qtable.get_values("----X----", "01") == {"01": 100.0}


def test_get_state_values_empty(qtable: QTable):
    """Test that the value of zero is correctly returned when trying to retrieve
    the value of an action that doesn't have a value in the Q-table"""
    assert qtable.table == {}  # Q-table is empty
    assert qtable.get_values("----X----") == {
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
    assert qtable.get_values("----X----", "00") == {"00": 0.0}


def test_get_state_values_all(qtable: QTable):
    """Test that all action values are returned when querying the value of a
    state without providing an action key"""
    qtable.table = {"----X----": {"01": 100.0}}  # Q-table is not empty
    assert qtable.get_values("----X----") == {
        "00": 0.0,
        "01": 100.0,
        "02": 0.0,
        "10": 0.0,
        "11": 0.0,
        "12": 0.0,
        "20": 0.0,
        "21": 0.0,
        "22": 0.0,
    }
