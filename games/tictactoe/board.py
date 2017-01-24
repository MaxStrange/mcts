"""
This module holds the TicTacToe game's Board class.
"""
import os

class Board:
    """
    This class represents the game's board.
    """
    def __init__(self):
        top =    [" ", " ", " "]
        middle = [" ", " ", " "]
        bottom = [" ", " ", " "]
        self._rows = [top, middle, bottom]

    def __str__(self):
        s = os.linesep
        s += " " * 3 + self._rows[0][0] + " | " + self._rows[0][1] + " | "+\
                self._rows[0][2]
        s += os.linesep
        s += "-----" * 3
        s += os.linesep
        s += " " * 3 + self._rows[1][0] + " | " + self._rows[1][1] + " | "+\
                self._rows[1][2]
        s += os.linesep
        s += "-----" * 3
        s += os.linesep
        s += " " * 3 + self._rows[2][0] + " | " + self._rows[2][1] + " | "+\
                self._rows[2][2]
        return s

    def place(self, move, symbol):
        """
        Places the given symbol on the board at the given location.
        """
        assert(symbol == 'x' or symbol == 'o')
        assert(self.valid_move(move))

        r, c = move
        self._rows[r][c] = symbol

    def three_in_a_row(self):
        """
        Returns True if x or if o has three in a row.
        Also returns who won if there is a winner (otherwise returns None).
        """
        rows, winner = self._check_for_three(self._rows)
        if rows:
            return True, winner
        cols, winner = self._check_for_three(self._cols())
        if cols:
            return True, winner
        diagonals, winner = self._check_for_three(self._diagonals())
        if diagonals:
            return True, winner

        return False, None

    def valid_move(self, move):
        """
        Checks the given row, col tuple for validity in the game board.
        """
        r, c = move
        try:
            spot = self._rows[r][c]
            return spot == ' '
        except IndexError:
            return False

    def _check_for_three(self, ls):
        for row_col_or_diag in ls:
            s = 0
            for spot in row_col_or_diag:
                s += self._evaluate(spot)
            if s is 3:
                return True, 'x'
            elif s is -3:
                return True, 'o'
        return False, ' '

    def _cols(self):
        """
        Returns a generator that generates each column.
        """
        yield [row[0] for row in self._rows]
        yield [row[1] for row in self._rows]
        yield [row[2] for row in self._rows]

    def _diagonals(self):
        """
        Returns a generator that generates each diagonal.
        """
        yield [self._rows[0][0], self._rows[1][1], self._rows[2][2]]
        yield [self._rows[0][2], self._rows[1][1], self._rows[2][0]]

    def _evaluate(self, spot):
        """
        Evaluates a spot, giving a 1 if it is an 'x', a -1 if it is an 'o'
        and a 0 if it is neither.
        """
        if spot == 'x':
            return 1
        elif spot == 'o':
            return -1
        else:
            return 0



