import unittest
from unittest.mock import patch, mock_open
from unogame import UnoGame
import pickle

class TestUnoGame(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh instance of UnoGame before each test."""
        self.game = UnoGame()

    def test_add_players(self):
        """Test adding a player to the game."""
        with patch('builtins.input', side_effect=['Alice']):
            self.game.add_players()
        self.assertIn('Alice', self.game.players)
        self.assertIn('Alice', self.game.winners)
        self.assertEqual(self.game.players['Alice'], 0)
        self.assertEqual(self.game.winners['Alice'], 0)

    def test_add_score(self):
        """Test adding a score and checking for game completion."""
        self.game.players = {'Alice': 0, 'Bob': 0}
        self.game.winners = {'Alice': 0, 'Bob': 0}

        with patch('builtins.input', side_effect=['Alice', '50']):
            self.game.add_score()

        self.assertEqual(self.game.players['Alice'], 50)
        self.assertFalse(self.game.game_complete)

        with patch('builtins.input', side_effect=['Alice', '300']):
            self.game.add_score()

        self.assertTrue(self.game.game_complete)
        self.assertEqual(self.game.winners['Alice'], 1)

    def test_show_scores(self):
        """Test showing scores does not raise exceptions."""
        self.game.players = {'Alice': 100, 'Bob': 200}
        with patch('builtins.print') as mocked_print:
            self.game.show_scores()
        mocked_print.assert_any_call("Alice has scored 100 points.")
        mocked_print.assert_any_call("Bob has scored 200 points.")

    def test_reset_scores(self):
        """Test resetting all player scores."""
        self.game.players = {'Alice': 100, 'Bob': 200}
        self.game.reset_scores()
        self.assertEqual(self.game.players['Alice'], 0)
        self.assertEqual(self.game.players['Bob'], 0)

    def test_save_game(self):
        """Test saving the game state to a file."""
        mock_file = mock_open()
        with patch('builtins.open', mock_file), patch('pickle.dump') as mock_pickle:
            self.game.save_game()
            mock_file.assert_called_once_with("uno_game.pkl", "wb")
            mock_pickle.assert_called_once_with(self.game, mock_file())

    def test_load_game(self):
        """Test loading the game state from a file."""
        mock_file = mock_open()
        mock_game = UnoGame()
        with patch('builtins.open', mock_file), patch('pickle.load', return_value=mock_game):
            loaded_game = UnoGame.load_game()
            self.assertEqual(loaded_game, mock_game)

    def test_show_winner_results(self):
        """Test showing winner results does not raise exceptions."""
        self.game.winners = {'Alice': 2, 'Bob': 1}
        with patch('builtins.print') as mocked_print:
            self.game.show_winner_results()
        mocked_print.assert_any_call("Alice has won 2 times.")
        mocked_print.assert_any_call("Bob has won 1 times.")

if __name__ == "__main__":
    unittest.main()