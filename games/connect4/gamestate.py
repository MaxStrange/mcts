"""
Module to hold the Connect4 GameState class.
"""
import copy
from games.connect4.board import Board
import os

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

    def __str__(self):
        s = "State: "
        for key, val in self.__dict__.items():
            s += os.linesep + "    " + key + ": " + str(val)
        return s

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            # We can't serialize _ai because it is a module
            if k == "_ai":
                setattr(result, k, v)
            else:
                setattr(result, k, copy.deepcopy(v, memo))
        return result

    def current_player_symbol(self):
        """
        Gets the current player's symbol
        """
        if self.players_turn:
            return self._metadata.players_symbol
        else:
            return self._metadata.ai_symbol

    def game_over(self):
        """
        Returns True if the game is over, False if it is not.
        """
        there_is_a_winner, winner = self._board.three_in_a_row()
        self.winner = winner
        if len(self.possible_moves()) == 0:
            # There is a draw, rather than a winner
            there_is_a_winner = True
            self.winner = ' '
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
                            "gone there? Index ranges are 0 to 5 and 0 to 6."
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

    def possible_moves(self):
        """
        Returns the set of all actions that lead to a legal next turn from
        the current state.
        """
        return [move for move in self._action_set()\
                if self._board.valid_move(move)]

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
        move = self._ai.get_best_move(self, _evaluation_function)
        self._board.place(move, self._metadata.ai_symbol)
        self._move_that_derived_this_state = move
        self._incoming_move = None
        self.players_turn = True

    def take_turn(self, move):
        """
        This function can be used to take a turn when the caller does
        not know whose turn it is or does not want to worry about it.
        In general, this function is to be used for deriving new states
        in a search tree, and should probably not be used as part of the
        UI's calls.
        """
        if self.players_turn:
            self._board.place(move, self._metadata.player_symbol)
            self.players_turn = False
        else:
            self._board.place(move, self._metadata.ai_symbol)
            self.players_turn = True
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
        self.players_turn = False

    def _action_set(self):
        """
        Generates all possible actions. Does not pay attention to
        whether they are legal or not for the current game state.
        """
        for r in range(6):
            for c in range(7):
                yield((r, c))

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



def _evaluation_function(state):
    """
    Evaluates how good the position is for the current player.
    """
    reward = 0
    if state._metadata.ai_symbol == 'x' and state.winner == 'x':
        reward = 1.0
    elif state._metadata.ai_symbol == 'o' and state.winner == 'o':
        reward = 1.0
    elif state._metadata.ai_symbol == 'x' and state.winner == 'o':
        reward = 0.0
    elif state._metadata.ai_symbol == 'o' and state.winner == 'x':
        reward = 0.0
    else:
        reward = 0.5

    return reward

