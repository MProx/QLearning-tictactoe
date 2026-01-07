import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.games.tictactoe import Board


@pytest.fixture
def board():
    return Board()


def test_as_str(board: Board) -> None:
    """Test that the as_str() method generates a string representation of the
    board"""

    board.cells[1].marker = "X"
    board.cells[5].marker = "O"
    board.cells[8].marker = "X"

    assert board.as_str() == "-X---O--X"


@pytest.mark.parametrize("row,col", [(0, 0), (1, 0), (2, 2)])
def test_get_cell(board: Board, row, col) -> None:
    "Test that the correct cell is returned by the get_cell() method"
    idx = 3 * row + col
    board.cells[idx].marker = "X"
    cell = board.get_cell(row, col)
    assert cell.row == row
    assert cell.col == col
    assert cell.marker == "X"


def test_get_cell_bad_coords(board: Board) -> None:
    """Test that an exception is raised when a cell's coordinates don't match
    it's attributes"""
    row = 2
    col = 1
    idx = 3 * row + col
    board.cells[idx].marker = "X"
    board.cells[idx].row = 0  # <- Break cell

    with pytest.raises(RuntimeError):
        board.get_cell(row, col)


def test_str(board: Board) -> None:
    """Test that the __str__() method works which prints the board as a grid. E.g.:
    X| |O
    -----
     |X|
    -----
     | |O
    """
    board.cells[0].marker = "X"
    board.cells[2].marker = "O"
    board.cells[4].marker = "X"
    board.cells[8].marker = "O"
    assert str(board) == ("X| |O\n-----\n |X| \n-----\n | |O")
