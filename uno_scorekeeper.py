"""
A script to manage and play a game of Uno using the `UnoGame` class.

This script provides functionality to:
- Load a previously saved game state or start a new game.
- Manage game rounds and scores using the `UnoGame` class.
- Allow players to continue playing multiple games in succession.
- Save the current game state upon quitting.

Usage:
    - The script will prompt the user to load a saved game or start a new one.
    - Players can continue to play rounds until they decide to quit.
    - The game state can be saved for resumption at a later time.

Flow:
    1. The user is prompted to load a saved game or start a new one.
    2. The game continues until the user decides to quit.
    3. Upon quitting, the user has the option to save the current game state.

Dependencies:
    - `UnoGame` class from the `unogame` module.

Attributes:
    game (UnoGame): An instance of the UnoGame class managing the current game state.
"""

from unogame import UnoGame

# Initialize the game state
i = False
game = UnoGame()

# Prompt the user to load a saved game or start a new one
while not i:
    load = input("Do you want to load a previous game? (y/n)")
    if load not in ['y', 'n']:
        print("Invalid input.")
    elif load == 'y':
        loaded = game.load_game()
        if loaded is not None:
            game = game.load_game()
        i = True
    else:
        i = True

# Main game loop
ended = False
while not ended:
    game.score_keeper() # Manage the rounds and scores
    if game.quit_condition:
        ended = True
    else:
        another_one = input("Do you want to keep playing? (y/n)")
        if another_one == "n":
            game.show_winner_results() # Show the overall results
            save = input("Do you want to save the game state? (y/n)")
            if save == 'y':
                game.game_complete = False
                game.save_game() # Save the game state
            ended = True
        else:
            game.game_complete = False
            print(f"Starting game {game.game}")
