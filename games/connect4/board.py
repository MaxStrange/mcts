"""
This module holds the connect 4 game's Board class.
"""
import os

class Board:
    """
    This class represents the game's board.
    """
    def __init__(self):
        self._rows = []
        for row_index in range(6):
            row = [" " for _ in range(7)]
            self._rows.append(row)

    def __str__(self):
        s = os.linesep
        for row in self._rows:
            row_str = ""
            for spot in row:
                row_str += spot
            s += row_str + os.linesep
        return s

    def place(self, move, symbol):
        """
        Places the given symbol on the board at the given location.
        """
        assert(symbol == 'x' or symbol == 'o')
        assert(self.valid_move(move))

        r, c = move
        self._rows[r][c] = symbol

    def four_in_a_row(self):
        """
        Returns True if x or if o has four in a row.
        Also returns who won if there is a winner (otherwise None).
        """
        rows, winner = self._check_for_four(self._rows)
        if rows:
            return True, winner
        cols, winner = self._check_for_four(self._cols())
        if cols:
            return True, winner
        diag, winner = self._check_for_four(self._cols())
        if diag:
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

    def _check_for_four(self, ls):
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
        for i in range(7):
            yield [row[i] for row in self._rows]

    def _diagonals(self):
        for j in range(3, 9):
            yield [self._rows[i][j - i] for i in range(len(self._rows))]

        for j in range(-2, 3):
            yield [self._rows[i][i + j] for i in range(len(self._rows))]

    def _evaluate(self, spot):
        """
        Evaluates a spot, giving a 1 if it is an 'x', a -1 if it is an 'o' and
        a 0 if it is neither.
        """
        if spot == 'x':
            return 1
        elif spot == 'o':
            return -1
        else:
            return 0








