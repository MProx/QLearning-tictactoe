import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.games.tictactoe import IllegalMoveError, TicTacToe


@pytest.fixture
def game() -> TicTacToe:
    return TicTacToe()


def test_get_all_valid_moves(game: TicTacToe) -> None:
    """Test that valid moves can be identifie"""
    # Mark some cells as occupied
    game.board.cells[0].marker = "X"
    game.board.cells[2].marker = "O"
    game.board.cells[4].marker = "X"
    game.board.cells[8].marker = "O"

    # Test that the remainder are returned:
    expected = [(0, 1), (1, 0), (1, 2), (2, 0), (2, 1)]
    assert game.get_all_valid_moves() == expected


@pytest.mark.parametrize("row,col", [(0, 0), (1, 0), (2, 2)])
def test_place_marker_legal(game: TicTacToe, row, col) -> None:
    """Test that the TicTacToe.play_move() can place markers in legal
    positions"""
    c = game.board.get_cell(row, col)
    assert c.marker is None
    game.play_move("X", row, col)
    assert c.marker == "X"
    c_new = game.board.get_cell(row, col)
    assert c_new.marker == "X"


@pytest.mark.parametrize(
    "marker,row,col,exception_raised",
    [
        ("A", 0, 0, ValueError),  # invalid marker
        ("X", 3, 0, ValueError),  # Out of bounds
        ("O", 0, -1, ValueError),  # Out of bounds
        ("O", 0, 3, ValueError),  # Out of bounds
        ("O", -1, 1, ValueError),  # Out of bounds
        ("O", 3, 1, ValueError),  # Out of bounds
        ("X", 1, 1, IllegalMoveError),  # cell already occupied
    ],
)
def test_place_marker_illegal(
    game: TicTacToe, marker, row, col, exception_raised
) -> None:
    """Test that the TicTacToe.play_move() can't place invalid markers, or valid
    markers in illegal positions"""
    game.board.cells[4].marker = "X"

    with pytest.raises(exception_raised):
        game.play_move(marker, row, col)


def test_place_marker_game_over(game: TicTacToe) -> None:
    """Test that the TicTacToe.play_move() can place markers after the game has
    ended with a winner"""
    # Player X has won (one complete row)
    game.board.cells[0].marker = "X"
    game.board.cells[1].marker = "X"
    game.board.cells[2].marker = "X"

    with pytest.raises(IllegalMoveError):
        game.play_move("O", 0, 0)


def test_place_marker_draw(game: TicTacToe) -> None:
    """Test that the TicTacToe.play_move() can place markers after the game has
    ended in a drae"""
    # Fill all game states in a way that there is no winner:
    # X|O|X
    # O|X|O
    # O|X|O

    x_coords = [(0, 0), (0, 2), (1, 1), (1, 2), (2, 1)]
    for row, col in x_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "X"
    o_coords = [(0, 1), (1, 0), (2, 0), (2, 2)]
    for row, col in o_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "O"

    with pytest.raises(IllegalMoveError):
        game.play_move("O", 0, 0)


def test_game_over_horizontal_winner(game: TicTacToe) -> None:
    """Check that the game.over() method correctly identifies terminal games
    when there's a horizontal row of the same marker"""
    # Horizontal line across the middle row:
    game.board.cells[3].marker = "X"
    game.board.cells[4].marker = "X"
    game.board.cells[5].marker = "X"
    # Opponent positions:
    game.board.cells[2].marker = "O"
    game.board.cells[7].marker = "O"

    assert game.is_over()
    assert game.winner == "X"


def test_game_over_vertical_winner(game: TicTacToe) -> None:
    """Check that the game.over() method correctly identifies terminal games
    when there's a vertical row of the same marker"""
    # Vertical line down the middle row:
    game.board.cells[1].marker = "X"
    game.board.cells[4].marker = "X"
    game.board.cells[7].marker = "X"
    # Opponent positions:
    game.board.cells[0].marker = "O"
    game.board.cells[8].marker = "O"

    assert game.is_over()
    assert game.winner == "X"


def test_game_over_diagonal(game: TicTacToe) -> None:
    """Check that the game.over() method correctly identifies terminal games
    when there's a diagonal row of the same marker"""
    # Diagonal line of Xs:
    game.board.cells[0].marker = "X"
    game.board.cells[4].marker = "X"
    game.board.cells[8].marker = "X"
    # Opponent positions:
    game.board.cells[1].marker = "O"
    game.board.cells[5].marker = "O"

    assert game.is_over()
    assert game.winner == "X"


def test_game_over_draw(game: TicTacToe) -> None:
    """Check that the game.over() method correctly identifies terminal games
    when there's a draw (no winner but no more available moves)"""

    # Fill all game states in a way that there is no winner:
    # X|O|X
    # O|X|O
    # O|X|O

    x_coords = [(0, 0), (0, 2), (1, 1), (1, 2), (2, 1)]
    for row, col in x_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "X"
    o_coords = [(0, 1), (1, 0), (2, 0), (2, 2)]
    for row, col in o_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "O"

    assert game.is_over()
    assert game.winner is None


def test_game_over_negative(game: TicTacToe) -> None:
    """Check that the game.over() method correctly identifies non-terminal
    games"""

    # Fill all game states in a way that there is no winner:
    # X| |X
    # O|X|
    # O| |O

    x_coords = [(0, 0), (0, 2), (1, 1)]
    for row, col in x_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "X"
    o_coords = [(1, 0), (2, 0), (2, 2)]
    for row, col in o_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "O"

    assert not game.is_over()
    assert game.winner is None


def test_game_over_cached(game: TicTacToe) -> None:
    """Check that the game.over() method correctly uses its cache"""

    # Fill all game states in a way that there is no winner:
    # X| |X
    # O|X|
    # O| |O
    x_coords = [(0, 0), (0, 2), (1, 1)]
    for row, col in x_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "X"
    o_coords = [(1, 0), (2, 0), (2, 2)]
    for row, col in o_coords:
        cell = game.board.get_cell(row, col)
        cell.marker = "O"

    # Modify the cached results to indicate that there is a winner when there
    # actually isn't:
    game.complete = True
    game.winner = "X"

    assert game.is_over()
    assert game.winner == "X"
