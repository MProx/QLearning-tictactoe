from pathlib import Path

from src.agents import QLearningAgent
from src.exceptions import IllegalMoveError
from src.games import TicTacToe


class CLI:
    def __init__(self, game: TicTacToe) -> None:
        self.game = game

    def show_board(self) -> None:
        print(self.game.board)

    def get_player_move(self) -> tuple[int, int]:
        answer = input("Pick a row and column separated by a comma: ")
        row, col = [int(i.strip()) for i in answer.split(",")]
        print(f"You chose {row} and {col}")
        return row, col

    def show_opponent_move(self, row: int, col: int) -> None:
        print(f"Your opponent chose {row} and {col}")

    def report_illegal_move(self) -> None:
        print("That's an illegal move. Try again.")

    def player_won(self) -> None:
        print("You won!")

    def player_lost(self) -> None:
        print("You lost :(")

    def draw(self) -> None:
        print("It's a draw")


class Play:
    def __init__(self):
        self.game = TicTacToe()
        self.computer_player = QLearningAgent()
        self.computer_player.load(Path("saves/agent_o_q_table.csv"))
        self.cli = CLI(game=self.game)

    def run(self):
        while not self.game.is_over():
            self.cli.show_board()
            # Human player's turn:
            while True:
                try:
                    row, col = self.cli.get_player_move()
                    self.game.play_move("X", row, col)
                except IllegalMoveError:
                    self.cli.report_illegal_move()
                else:
                    break

            if self.game.is_over():
                break

            # Computer player's turn:
            start_state = self.game.board.as_str()
            all_valid_moves = self.game.get_all_valid_moves()
            row, col = self.computer_player.select_action(start_state, all_valid_moves)
            self.cli.show_opponent_move(row, col)
            self.game.play_move("O", row, col)

            if self.game.is_over():
                break

        self.cli.show_board()
        if self.game.winner == "X":
            self.cli.player_won()
        elif self.game.winner == "O":
            self.cli.player_lost()
        else:
            self.cli.draw()


def main():
    play = Play()
    play.run()


if __name__ == "__main__":
    main()
