import argparse
import cProfile
import random
from pathlib import Path

from tqdm import tqdm

from src.agents import Agent, QLearningAgent
from src.games import TicTacToe


def configure_cli_args():
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument(
        "-n",
        "--n-episodes",
        type=int,
        default=10000,
        help="Number of episodes to train on. Default=100000",
    )
    parser.add_argument(
        "--skip-save",
        action="store_true",
    )
    args = parser.parse_args()
    return args


def main(n_episodes: int, skip_save: bool) -> None:
    player_x = QLearningAgent()
    player_o = QLearningAgent()

    for episode_idx in tqdm(range(n_episodes)):
        alpha = 1.0 - episode_idx / n_episodes  # Alpha decays to zero
        play_episode(alpha, player_x=player_x, player_o=player_o)
    if not skip_save:
        player_x.save(Path("saves/agent_x_q_table.csv"))
        player_o.save(Path("saves/agent_o_q_table.csv"))


def play_episode(
    alpha: float,
    player_x: Agent,
    player_o: Agent,
) -> None | str:
    """
    Alternate between each player starting with X until the game is over

    Arguments:
    alpha (float): probability of choosing a random action instead of following
    the policy.

    Returns:
    The marker of the winner ("X" or "O") or None if the game ends in a draw.
    """

    # The "new state" for the markov chain isn't after the player plays their
    # move, but rather after the opponent plays their following move (unless
    # the game is terminal). So we need to keep track of the previous states.
    prev_player: None | Agent = None
    prev_state: None | str = None
    prev_action: None | tuple[int, int] = None

    game = TicTacToe()
    while not game.is_over():
        for player in [player_x, player_o]:
            marker = "X" if player == player_x else "O"

            # Observe the state:
            start_state = game.board.as_str()
            all_valid_moves = game.get_all_valid_moves()

            # Decide between exploration or exploitation:
            if random.random() > alpha:
                row, col = player.select_action(start_state, all_valid_moves)
            else:
                row, col = random.choice(all_valid_moves)

            # Apply selected move:
            game.play_move(marker=marker, row=row, col=col)

            # Determine reward if any
            if game.is_over():
                # Train this player. Assign reward if it won, else mild punishment
                # if it's a draw (can't lose on your own round)
                player.update(
                    start_state=start_state,
                    action=(row, col),
                    reward=1 if game.winner == marker else -0.2,
                    new_state=game.board.as_str(),
                    done=True,
                )
                # Train opponent player with bigger punishment if they lost, and
                # mild punishment if it's a draw (opponent can't win since it's not
                # their turn):
                if (
                    (prev_player is not None)
                    and (prev_state is not None)
                    and (prev_action) is not None
                ):
                    prev_player.update(
                        start_state=prev_state,
                        action=prev_action,
                        reward=-0.2 if game.winner is None else -1,
                        new_state=game.board.as_str(),
                        done=True,
                    )

                # End episode immediately (don't let other player have a go)
                break
            else:
                # Apply OPPONENT's update method with new state:
                if (
                    (prev_player is not None)
                    and (prev_state is not None)
                    and (prev_action) is not None
                ):
                    prev_player.update(
                        start_state=prev_state,
                        action=prev_action,
                        reward=0,  # always zero for non-terminal states
                        new_state=game.board.as_str(),
                        done=False,
                    )

                # Save for next training round:
                prev_player = player
                prev_state = start_state
                prev_action = (row, col)

    return game.winner


if __name__ == "__main__":
    args = configure_cli_args()
    cProfile.run(
        "main(n_episodes=args.n_episodes, skip_save=args.skip_save)",
        sort="tottime",
    )
