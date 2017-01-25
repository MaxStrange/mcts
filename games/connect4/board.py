"""
This module holds the connect 4 game's Board class.
"""
import os

class Board:
    """
    This class represents the game's board.

    IMPORTANT:
    A board has its rows indexed from 0, starting from the BOTTOM.
    """
    def __init__(self):
        self._rows = []
        for row_index in range(6):
            row = [" " for _ in range(7)]
            self._rows.append(row)

    def __str__(self):
        nl = os.linesep
        s = nl
        for row in reversed(self._rows):
            row_str = ""
            for spot in row:
                if spot == ' ':
                    row_str += "|___"
                else:
                    row_str += "|_" + spot + "_"
            row_str += "|" + nl
            s += row_str
        rng = [str(i) for i in range(7)]
        nums = "   ".join(rng)
        s += nl + "  " + nums
        return s

    def place(self, move, symbol):
        """
        Places the given symbol on the board at the given location.
        """
        assert(symbol == 'x' or symbol == 'o')
        assert(self.valid_move(move))
        r = self._find_row_from_col(move)
        self._rows[r][move] = symbol

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
        diag, winner = self._check_for_four(self._diagonals())
        if diag:
            return True, winner

        return False, None

    def valid_move(self, move):
        """
        Checks the given row, col tuple for validity in the game board.
        """
        return not self._column_is_full(move)

    def _check_for_four(self, ls):
        for row_col_or_diag in ls:
            num_in_a_row = 0
            last_seen = None
            for spot in row_col_or_diag:
                if spot == last_seen and spot != ' ':
                    num_in_a_row += 1
                else:
                    last_seen = spot
                if num_in_a_row >= 3:
                    return True, last_seen
        return False, ' '

    def _column_is_full(self, col_index):
        column = [row[col_index] for row in self._rows]
        for spot in column:
            if spot == ' ':
                return False
        return True

    def _cols(self):
        for i in range(7):
            yield [row[i] for row in self._rows]

    def _diagonals(self):
        for j in range(3, 9):
            yield [self._rows[i][j - i] for i in range(len(self._rows))\
                    if (j - i) < 7 and (j - i) >= 0]

        for j in range(-2, 3):
            yield [self._rows[i][i + j] for i in range(len(self._rows))\
                    if (i + j) < 7 and (i + j) >= 0]

    def _find_row_from_col(self, col_index):
        """
        Finds the right row from the given column
        """
        column = [row[col_index] for row in self._rows]
        for i, spot in enumerate(column):
            # Looking from the bottom row up
            if spot == ' ':
                return i

        # If it ever gets here, this function is not implemented correctly
        assert(False)







