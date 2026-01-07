import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.games.tictactoe import Cell


@pytest.fixture
def cell():
    return Cell(1, 2)


def test_repr(cell: Cell) -> None:
    """test that the __repr__() method works correctly"""
    assert cell.__repr__() == "<Cell - row: 1, col:2, marker: None>"
    cell.marker = "X"
    assert cell.__repr__() == "<Cell - row: 1, col:2, marker: X>"


def test_is_empty(cell: Cell) -> None:
    """Test that the is_empty() method works"""
    assert cell.is_empty()
    cell.marker = "X"
    assert not cell.is_empty()


def test_set(cell: Cell) -> None:
    """Test that the set() method works"""
    assert cell.marker is None
    cell.set("X")
    assert cell.marker == "X"


def test_set_invalid(cell: Cell) -> None:
    """Test that a ValueError is raised when the set() method is used with
    something other than an "X" or an "O"."""
    with pytest.raises(ValueError):
        cell.set("FOOBAR")


@pytest.mark.parametrize(
    "marker,expected_string",
    [
        ("X", "X"),
        ("O", "O"),
        (None, " "),
    ],
)
def test_str(cell: Cell, marker, expected_string) -> None:
    """Test that the __str__() method works"""
    cell.marker = marker
    assert str(cell) == expected_string
