import unittest
from unittest.mock import patch, mock_open
from unogame import UnoGame
import uno_scorekeeper  # Replace with the actual script name if different

class TestMainScript(unittest.TestCase):
    
    @patch("builtins.input")
    @patch("builtins.print")
    @patch("unogame.UnoGame.load_game")
    def test_bad_input_in_yes_no_sections(self, mock_load_game, mock_print, mock_input):
        """Test handling of invalid inputs in yes/no prompts."""
        mock_load_game.return_value = None
        mock_input.side_effect = ['invalid', 'y', 'n']  # Invalid input, then valid inputs

        uno_scorekeeper.i = False
        uno_scorekeeper.game = UnoGame()

        with patch("uno_scorekeeper.UnoGame", UnoGame):
            while not uno_scorekeeper.i:
                load = mock_input()
                if load not in ['y', 'n']:
                    print("Invalid input.")
                    mock_print.assert_any_call("Invalid input.")
                elif load == 'y':
                    uno_scorekeeper.game = uno_scorekeeper.game.load_game()
                    uno_scorekeeper.i = True
                else:
                    uno_scorekeeper.i = True

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("unogame.UnoGame.load_game")
    def test_load_nonexistent_file(self, mock_load_game, mock_print, mock_input):
        """Test loading a game file that doesn't exist."""
        mock_load_game.side_effect = FileNotFoundError("File not found.")
        mock_input.side_effect = ['y']  # User chooses to load a game

        uno_scorekeeper.i = False
        uno_scorekeeper.game = UnoGame()

        with patch("uno_scorekeeper.UnoGame", UnoGame):
            while not uno_scorekeeper.i:
                load = mock_input()
                if load == 'y':
                    try:
                        uno_scorekeeper.game = uno_scorekeeper.game.load_game()
                    except FileNotFoundError:
                        print("File not found.")
                        mock_print.assert_any_call("File not found.")
                        uno_scorekeeper.i = True
                else:
                    uno_scorekeeper.i = True

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("unogame.UnoGame.save_game")
    def test_save_on_quit(self, mock_save_game, mock_print, mock_input):
        """Test that the game state is saved when quitting."""
        mock_input.side_effect = ['n', 'y']  # User decides not to continue, then saves game

        uno_scorekeeper.ended = False
        uno_scorekeeper.game = UnoGame()
        uno_scorekeeper.game.quit_condition = True

        with patch("uno_scorekeeper.UnoGame", UnoGame):
            while not uno_scorekeeper.ended:
                if uno_scorekeeper.game.quit_condition:
                    save = mock_input()
                    if save == 'y':
                        uno_scorekeeper.game.save_game()
                        mock_save_game.assert_called_once()
                        mock_print.assert_any_call("Game state saved successfully.")
                        uno_scorekeeper.ended = True
                    else:
                        uno_scorekeeper.ended = True

if __name__ == "__main__":
    unittest.main()
