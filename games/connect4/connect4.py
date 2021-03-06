"""
This is the game logic for the Connect 4 game.
"""
from games.connect4.metadata import MetaData
from games.connect4.gamestate import GameState
import os


class ImproperUsageError(Exception):
    """
    An exception type to use when the programmer has used the API in an incorrect way.
    """
    pass

# Global variables
_metadata = MetaData()
_gamestate = None

def game_over():
    """
    Returns True if the game is over, False if it is not.
    """
    return _gamestate.game_over()


def get_ending_msg():
    """
    Returns the ending message (such as who won).
    """
    winner = _gamestate.get_winner()
    if winner == ' ':
        s = "IT'S A DRAW" + os.linesep
    else:
        s = winner + " WINS!" + os.linesep
    s += "Thanks for playing!"
    return s


def get_formatted_display():
    """
    Returns the state of the game as a string that can be printed to
    the console so that the user can understand what is currently
    happening in this game.
    """
    return _gamestate.get_formatted_display()


def get_input_request_str():
    """
    Returns the next string that the UI should print in order to request
    the next player turn information.
    """
    return _gamestate.get_next_input_request_str()


def get_next_metadata_request_str():
    """
    Returns the next string that the UI should print in order to request
    the next metadata variable that the game requires.
    """
    global _metadata
    return _metadata.get_next_request_str()


def info_not_valid(info):
    """
    Returns True if the given info is NOT valid for the game state's
    current request for player info.
    """
    valid, err_msg = _gamestate.info_valid(info)
    return (not valid, err_msg)


def initialize(ai_module):
    """
    Runs any initialization code necessary for the game.
    This is run after all meta data is collected.
    """
    if not _metadata:
        raise ImproperUsageError("Initialize should only be called " +\
                "after metadata has been fully collected")
    else:
        global _gamestate
        _gamestate = GameState(_metadata, ai_module)


def metadata_not_valid(d):
    """
    Returns True if the data item is NOT valid.
    """
    return not _metadata.valid(d)


def needs_more_metadata():
    """
    Returns whether or not the game logic requires any more meta data.
    """
    return _metadata.needs_more_metadata()


def needs_more_player_input():
    """
    Returns whether or not the game logic requires any more player input
    to execute his/her turn.
    """
    return _gamestate.needs_more_player_input()


def players_turn():
    """
    Returns True if it is the player's turn, Flase if it is the computer's
    turn instead.
    """
    return _gamestate.players_turn


def set_next_input(info):
    """
    Sets the next item in the game state.
    """
    _gamestate.set_next_input(info)


def set_next_metadata(d):
    """
    Sets the next item to d in the game's meta data.
    """
    _metadata.set_next_metadata(d)


def take_ai_turn():
    """
    Modifies the game state so that the computer has taken its turn.
    """
    _gamestate.take_ai_turn()


def take_player_turn():
    """
    Modifies the game state so that the plaher has taken his/her turn.
    """
    _gamestate.take_player_turn()


def welcome_string():
    """
    Returns the welcome string.
    """
    return "Welcome to Connect4!"









