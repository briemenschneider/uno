import pickle


class UnoGame:
    """
    A class to manage a game of Uno, including players, scores, rounds, and saving/loading game state.

    This class provides methods to add players, manage scores, display results, and handle the game state for multiple rounds and games. It also supports saving the game state to a file and loading it later.

    Attributes:
        winners (dict): Tracks the number of games won by each player.
        players (dict): Tracks the current scores of all players.
        round (int): The current round number.
        game (int): The current game number.
        game_complete (bool): Indicates whether the current game has been completed.
        quit_condition (bool): Indicates whether the player has chosen to quit the game.
        initialized (bool): Tracks whether the game has been initialized with players.

    Methods:
        add_players(): Adds a new player to the game.
        add_score(): Updates the score for a round and checks if a player has won the game.
        show_scores(): Displays the current scores of all players.
        score_keeper(): Manages the game, including adding players, recording scores, and resetting for new games.
        show_winner_results(): Displays the total wins for each player.
        reset_scores(): Resets the scores of all players to zero.
        save_game(): Saves the current game state to a file using pickle.
        load_game(): Loads a previously saved game state from a file.
    """
    def __init__(self):
        self.winners = {}
        self.players = {}
        self.round = 1
        self.game = 1
        self.game_complete = False
        self.quit_condition = False
        self.initialized = False

    def add_players(self):
        """
        Prompts the user to add a new player to the game.

        Adds the player's name to the `players` dictionary with an initial score of 0 
        and to the `winners` dictionary with an initial win count of 0.
        """
        new_player = input("Enter the name of the player, then hit enter: ")
        self.players[new_player] = 0
        self.winners[new_player] = 0

    def add_score(self):
        """
        Records the score for a round and updates the game state.

        Prompts the user to enter the winner's name and score for the round. 
        If the winner's total score exceeds 300, the round is declared complete, 
        and the game status is updated. If the user enters 'q', the game state is saved, 
        and the quit condition is set.

        Raises:
            ValueError: If the entered score is not a valid integer.
        """
        success = False
        while not success:
            winner = input("Enter the winner's name or 'q' to save and quit: ")
            if winner == 'q':
                self.save_game()
                self.quit_condition = True
                return
            if winner not in self.players:
                print("Enter a valid player.")
                continue
            new_score = input("Enter the winning score: ")
            self.players[winner] = self.players[winner] + int(new_score)
            if self.players[winner] >= 300:
                print(f"Round is complete. {winner} is the winner!")
                self.show_scores()
                self.winners[winner] += 1
                self.game_complete = True
            else:
                self.round = self.round + 1
                print(f"Continue playing, round {self.round}.")
            success = True

    def show_scores(self):
        """
        Displays the current scores of all players.

        Iterates through the `players` dictionary and prints each player's name 
        along with their current score.
        """
        for key, value in self.players.items():
            print(f"{key} has scored {value} points.")

    def score_keeper(self):
        """
        Manages the main flow of the Uno game, including rounds and games.

        Handles the initialization of players, displays current scores, 
        and manages rounds until a game is completed or the quit condition is met.

        Behavior:
            - If the game is not initialized, prompts the user to add players.
            - Displays the current round and scores.
            - Handles score updates and checks for game completion.
            - Resets scores and increments the game count upon game completion.
        """
        if not self.initialized:
            done = False
            while not done:
                print("Press 1 to add a player")
                print("Press 2 when done to continue")
                choice = input("Choice: ")
                if choice == str(1):
                    self.add_players()
                elif choice == str(2):
                    done = True
                else:
                    print("Invalid input.")
            self.initialized = True
        print(f"Current round is {self.round}")
        while not self.game_complete and not self.quit_condition:
            self.show_scores()
            self.add_score()
        self.round = 1
        self.reset_scores()
        self.game = self.game + 1

    def show_winner_results(self):
        """
        Displays the total number of wins for each player.

        Iterates through the `winners` dictionary and prints each player's name 
        along with the number of games they have won.
        """
        print("Winning numbers:")
        for key, value in self.winners.items():
            print(f"{key} has won {value} times.")

    def reset_scores(self):
        """
        Resets all player scores to zero.

        Iterates through the `players` dictionary and sets the score for 
        each player to 0, preparing for the next game.
        """
        for key, value in self.players.items():
            self.players[key] = 0
    
    def save_game(self):
        """
        Saves the current game state to a file.

        Serializes the current instance of the game using pickle and writes it to 
        a file named "uno_game.pkl".

        Raises:
            FileNotFoundError: If the file cannot be created.
            IndexError: If there is an error during the serialization process.
        """
        try:
            with open("uno_game.pkl", "wb") as file:
                pickle.dump(self, file)
                file.close()
        except (FileNotFoundError, IndexError) as e:
            print(f"An error creating the file occurred: {e}")
    
    @classmethod
    def load_game(cls):
        """
        Loads a previously saved game state from a file.

        Reads the "uno_game.pkl" file, deserializes the contents, and returns the 
        loaded instance of `UnoGame`.

        Returns:
            UnoGame: The loaded game instance.

        Raises:
            FileNotFoundError: If the save file is not found.
            IndexError: If the file contents are invalid or empty.
        """
        try:
            with open("uno_game.pkl", "rb") as file:
                loaded = pickle.load(file)
                return loaded
        except (FileNotFoundError, IndexError) as e:
            print(f"File not found or was empty: {e}")