"""
Module to hold the Tic Tac Toe MetaData class.
"""

class MetaData:
    """
    The meta data required for the game of Tic Tac Toe.
    """
    def __init__(self):
        self.player_symbol = None
        self.player_goes_first = None

    def get_next_request_str(self):
        if not self.player_symbol:
            self._request = "self.player_symbol"
            return "Player Symbol (x or o):"
        elif self.player_goes_first is None:
            self._request = "self.player_goes_first"
            return "Player goes first? (y/n): "
        else:
            raise IndexError("Out of metadata request strings")

    def needs_more_metadata(self):
        if not self.player_symbol:
            return True
        elif self.player_goes_first is None:
            return True
        else:
            return False

    def set_next_metadata(self, d):
        """
        Requires that d be clean already.
        """
        if self._request == "self.player_symbol":
            self.player_symbol = d
        elif self._request == "self.player_goes_first":
            self.player_goes_first = True if d == 'y' else False
        else:
            raise IndexError("Out of metadata to set")

    def valid(self, d):
        """
        Checks if d is valid, given the last item to be requested.
        """
        if self._request == "self.player_symbol":
            return d == "x" or d == "o" or d == "X" or d == "O"
        elif self._request == "self.player_goes_first":
            return d == "y" or d == "Y" or d == "n" or d == "N"
        else:
            raise IndexError("Out of metadata validations")
