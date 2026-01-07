from dataclasses import dataclass, field

from src.exceptions import IllegalMoveError


@dataclass
class Cell:
    """
    One cell in the game board. The cell will have coordinates (row and col),
    and optionally a marker ("X", "O" or None) for what mark occupies it.
    """

    row: int
    col: int
    marker: None | str = None

    def __repr__(self):
        return f"<Cell - row: {self.row}, col:{self.col}, marker: {self.marker}>"

    def __str__(self):
        return " " if not self.marker else self.marker

    def is_empty(self) -> bool:
        return self.marker is None

    def set(self, marker: str):
        if marker not in ["X", "O"]:
            raise ValueError(f"Illegal marker: {marker}")
        self.marker = marker


@dataclass
class Board:
    """Class to keep track of the game board, and all the player marks that
    have been plced on it"""

    cells: list[Cell] = field(
        default_factory=lambda: [
            Cell(row=row, col=col) for row in range(3) for col in range(3)
        ]
    )

    def __str__(self):
        """Print the game board in human-readable way"""
        return (
            f"{self.cells[0]}|{self.cells[1]}|{self.cells[2]}\n"
            "-----\n"
            f"{self.cells[3]}|{self.cells[4]}|{self.cells[5]}\n"
            "-----\n"
            f"{self.cells[6]}|{self.cells[7]}|{self.cells[8]}"
        )

    def as_str(self):
        """Represent the game board as a string, e.g. X-O---OOX"""
        symbols = ["-" if cell.marker is None else cell.marker for cell in self.cells]
        return "".join(symbols)

    def get_cell(self, row: int, col: int) -> Cell:
        """Retrieve a specific cell by it's row and column index"""
        cell = self.cells[3 * row + col]
        if (cell.row != row) or (cell.col != col):
            raise RuntimeError("Cell coordinates don't match attributes!")
        return cell


class TicTacToe:
    def __init__(self) -> None:
        self.board = Board()
        self.complete: bool = False
        self.winner: None | str = None

    def get_all_valid_moves(self):
        """Return a list of all valid game moves in as a (row, col) tuple"""
        result = [
            (cell.row, cell.col) for cell in self.board.cells if cell.marker is None
        ]
        return result

    def play_move(
        self,
        marker: str,
        row: int,
        col: int,
    ) -> None:
        """
        Place the marker ("X" or "O") in the coordinates denoted by the row and
        column indexes. Top left is [0, 0].

        Raise ValueError for unrecognised marker or invalid coordinates.

        Raise IllegalMoveError if an illegal move is attempted.
        """
        if self.is_over():
            raise IllegalMoveError("Game is over")
        if marker not in ["X", "O"]:
            raise ValueError(f"Unrecognised marker: {marker}")
        if row < 0 or row > 2 or col < 0 or col > 2:
            raise ValueError(f"Move coordinates out of bounds: ({row}, {col})")
        cell = self.board.get_cell(row, col)
        if not cell.is_empty():
            raise IllegalMoveError(
                "Attempted to place a marker in a cell that is not empty"
            )

        cell.set(marker)

    def is_over(self) -> bool:
        """True if the game is over false if still in play"""

        if self.complete:
            return True

        winning_combos = (
            ((0, 0), (0, 1), (0, 2)),  # top row
            ((1, 0), (1, 1), (1, 2)),  # middle row
            ((2, 0), (2, 1), (2, 2)),  # bottom row
            ((0, 0), (1, 0), (2, 0)),  # left column
            ((0, 1), (1, 1), (2, 1)),  # middle column
            ((0, 2), (1, 2), (2, 2)),  # right column
            ((0, 0), (1, 1), (2, 2)),  # Diagonal #1
            ((2, 0), (1, 1), (0, 2)),  # Diagonal #2
        )

        win_possible: bool = False
        for combo in winning_combos:
            cells = [self.board.get_cell(*c) for c in combo]
            markers = [c.marker for c in cells]
            # Check if either player has won using this combo:
            for marker in ["X", "O"]:
                if all(m == marker for m in markers):
                    self.complete = True
                    self.winner = marker
                    return True
            # Check if either player could still win using this combo:
            if ("X" not in markers) or ("O" not in markers):
                win_possible = True

        # TODO: Optimise this. Run selected checks after marker is placed,
        # depending on where. No point checking all rows/cols if placed marker
        # cannot win on those.

        if not win_possible:
            self.complete = True
            self.winner = None
            return True

        return False
