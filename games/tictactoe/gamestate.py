"""
Module to hold the Tic Tac Toe GameState class.
"""
from games.tictactoe.board import Board

class GameState:
    """
    Class to hold the game's transient data.
    """
    def __init__(self, metadata, ai):
        self._metadata = metadata
        self._ai = ai

        self._board = Board()
        self.players_turn = self._metadata.player_goes_first
        self._incoming_move = None
        self._move_that_derived_this_state = None
        self.winner = None

    def game_over(self):
        """
        Returns True if the game is over, False if it is not.
        """
        there_is_a_winner, winner = self._board.three_in_a_row()
        self.winner = winner
        return there_is_a_winner

    def get_formatted_display(self):
        """
        Returns the current state of the game in a way that the player
        will see.
        """
        return str(self._board)

    def get_next_input_request_str(self):
        """
        Returns the next string that the UI should print in order
        to request the next player turn information.
        """
        return "Row and Column: "

    def get_winner(self):
        """
        Returns the winner of the game or None if no winner.
        """
        return self.winner

    def info_valid(self, info):
        """
        Returns True if the information given is valid for what we have
        requested from the player.
        Also returns a message to print in the case of invalid input.
        """
        # Since we only request a single item each turn,
        # we just need to check if it makes sense as a (row, column) tuple
        try:
            user_input = self._parse_player_input(info)
            # Check if the two items can both be interpreted as numbers
            f = lambda lr: "".join([c for c in lr if c.isdigit()])
            left = f(user_input[0])
            right = f(user_input[1])
            try:
                r = int(left)
                c = int(right)
                # Now check to make sure that the player can actually go
                # there
                valid = self._board.valid_move((r, c))
                if valid:
                    return True, ""
                else:
                    return False, "Invalid row and col. Have you already "\
                            "gone there? Index ranges are 0 to 2."
                return self._board.valid_move((r, c)), ""
            except ValueError:
                return False, "Please enter valid numbers for row and col"
        except ValueError:
            return False, "Please enter a row and a column delimited by "\
                    "either a space or a comma, example: 0, 1"

    def needs_more_player_input(self):
        """
        Returns True if the GameState object does not have enough
        player input to decide an action for the player.
        """
        # We only need a row and a column from the player
        return self._incoming_move is None

    def set_next_input(self, info):
        """
        Sets the player input that was last requested. This should only
        be called if the info has passed info_valid().
        """
        assert(self.info_valid(info))
        # There is only the one thing: the row and col pair
        parsed = self._parse_player_input(info)
        self._incoming_move = (int(parsed[0]), int(parsed[1]))

    def take_ai_turn(self):
        """
        Takes the computer's turn.
        """
        move = self._ai.get_best_move(self)
        self._board.place(move, self._metadata.ai_symbol)
        self._move_that_derived_this_state = move
        self._incoming_move = None

    def take_player_turn(self):
        """
        Takes the player's turn.
        """
        move = self._incoming_move
        self._board.place(move, self._metadata.player_symbol)
        self._move_that_derived_this_state = move
        self._incoming_move = None

    def _parse_player_input(self, info):
        """
        Attempts to parse the given info object into a tuple of the form
        (row, col). Raises a ValueError if this is impossible.
        Note though that this does not check if row and col are valid,
        just that they can be split up into two distinct values as a
        tuple.
        """
        user_input = info.strip().split(',')
        if len(user_input) is 1:
            # try splitting on a space, maybe they entered it as 0 1
            user_input = info.strip().split(' ')

        if len(user_input) is not 2:
            raise ValueError("Could not split user input")
        else:
            return (user_input[0], user_input[1])




