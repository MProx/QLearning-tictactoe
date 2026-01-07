# Tic-Tac-Toe

This repo shows an example of Q-learning. 

During training, two AI players (agents) dual againt each other to learn how to win the game.

During gameplay, the human user ("X") duals against an AI agent ("O"), which was trained in the previous step. 

## Usage

Requires `uv`package manager

Training:
```
uv run python3 train.py
```

Playing:
```
uv run python3 play.py
```

Running linting and unit tests:
```
cd scripts
chmod +x run_tests.sh
./run_tests.sh
```

## Q-learning 

The agents learn by maintaining and updating a Q table. Each row of the table represents a game state that the agent has encountered (denoted by a string representation of the game state). Columns in the table represent all available actions. In this case, they're the possible board positions on the 3 x 3 grid denoted by integer strings. "00" is the top left, "11" is the middle, "02" is the top right, etc. 

The elements of the table are populated with the "quality" of each state/action pair, which the agent learns as it plays. As the agents train they choose moves and observe the results (reward/pusihment and new state). Agents are rewarded for each game they win, and punished (negative reward) when they lose or if it's a draw. The `state` -> `action` -> `rewaard` -> `new state` progression is a hidden markov chain. 

Note, however, that the "new state" is not the state of after the agent plays their move. It is actually the state after the opponent has had a turn too. This is because the "new state" must be one that the agent might later encounter when deciding to play their own move. If training on "new states" immediately after playing their own move, then this cannot be true because it is not the player's own turn. This requires some trickery where we need to keep track of the previous players observed states and actions as we alternate between player moves. The exeption to this for terminal game states, where the reward is assigned immediately and the agent does not get another turn (there are no future states).

## Exploration vs exploitation
To discourage the agent settling on a suboptimal strategy during training (local minima), we introduce some randomness. In each game episide, we define a certain probability (alpha) with which the player might choose a random move instead of following the policy that they have learned thus far. In the beginning of training, the alpha is set to 1.0 (always act randomly) and it slowly reduces to zero as it advances through the assigned number of training episodes.

## State space size:
Since there are 9 game slots and each can be one of three states ("X", "O" or empty), there are 3^9=19683 possible combinations. But not all of these are valid moves. E.g. one of the ~19k states would be the whole board covered in Xs, which is an impossible state to wind up in since "O" will have had turns. Practically, even though tic-tac-toe is such a simple game, the state space ends up in about 2.5k rows in the Q-table. Clearly, this method of reinforcemnt learning is impractical in all but the most simple applications. 

As stated earlier, the Q-table (state space) is really just a lookup table for estimating the value of each state-action pair. As the agent gains experience with the game, the estimates of the quality of each move get better. For problems with a larger state space, deep learning is a better option than a lookup table to estimate the quality of each move. Deep learning networks have the advantage that they don't need to have experienced a particular environment state to be able to make predictions based on similar states it's seen before. If, for example, the state was a pixel array from an image instead of a tic-tac-toe board, then the deep learning model might still be able to predict the quality of each move in that state, even though it hasn't seen that precise image (state) before.

## Future improvements:
* Figure out some form of monitoring for training. Currently we just play a fixed number of games, but it would be nice to know when we've converged on a good solution and further training doesn't add value.
* Use deep learning (Deep Q Networks, or DQN) to estimate Q rather than use a loopup table. 
* Turn 'play' script into a UI instead of a CLI game. Web app maybe?
