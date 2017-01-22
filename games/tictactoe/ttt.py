"""
This is the game logic for the Tic Tac Toe game.
"""
from games.tictactoe.metadata import MetaData
from games.tictactoe.gamestate import GameState

class ImproperUsageError(Exception):
    """
    An exception type to use when the programmer has used the API
    in an incorrect way.
    """
    pass


# Global variables
_metadata = MetaData()
_gamestate = GameState()


def get_input_request_str():
    """
    Returns the next string that the UI should print in order to request
    the next player turn information.
    """
    global _gamestate
    return _gamestate.get_next_input_request_str()


def get_next_metadata_request_str():
    """
    Returns the next string that the UI should print in order to request
    the next metadata variable that the game requires.
    """
    global _metadata
    return _metadata.get_next_request_str()


def initialize():
    """
    Runs any initialization code necessary for the game.
    This is run after all meta data is collected.
    """
    if not _metadata:
        raise ImproperUsageError("Initialize should only be called " +\
                "after metadata has been fully collected")
    else:
        pass


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


def set_next_metadata(d):
    """
    Sets the next item to d in the game's meta data.
    """
    _metadata.set_next_metadata(d)


def welcome_string():
    """
    Returns the welcome string
    """
    return "Welcome to Tic Tac Toe!"










