# Board class containing the state of the board and commands pertaining to it
class Board:
    # Either 1 or 2
    signs = ('X', 'O')

    def __init__(self):
        # Represents 9 fields
        self.fields = [-1 for x in range(9)]

    # Reset the board to the inital state
    def resetBoard(self):
        self.fields = [-1 for x in range(9)]

    # Prints the board with 3 fields in each line
    def printBoard(self):
        fieldStr = ''
        for i in range(len(self.fields)):
            if i % 3 == 0 and i != 0:
                fieldStr += '\n'
            if self.fields[i] is -1:
                fieldStr += '[   ]'
            else:
                fieldStr += f'[ {self.signs[self.fields[i]]} ]'
        print(fieldStr)

    # Prints an example board with the index of each field
    def printExampleBoard(self, val=None):
        fieldStr = ''
        for i in range(len(self.fields)):
            if i % 3 == 0 and i != 0:
                fieldStr += '\n'
            if val is None:
                fieldStr += f'[{i % 3 + 1} {i // 3 + 1}]'
            else:
                fieldStr += f'[ {i} ]'
        print(fieldStr)

    # Returns a list of all free fields
    def freeFields(self, twoD=False):
        free = []
        for i, field in enumerate(self.fields):
            if field is -1:
                if twoD is False:
                    free.append(i)
                else:
                    free.append(self.oneDToTwoD(i))
        return free

    # Returns n'th row
    def row(self, n):
        i = n // 3
        return self.fields[i*3:i*3 + 3]

    # Returns n'th column
    def column(self, n):
        i = n % 3
        return self.fields[i::3]

    # Returns one of the two diagonals
    # n=0 is a downward diagonal, n=1 an upward diagonal
    def diagonal(self, n):
        # The formula ensures the direction of the slope
        return self.fields[n*6:9 - n*8:4 - n*6]

    # Translates 2D index to 1D index
    @staticmethod
    def twoDToOneD(x, y, width=3):
        return x + y*width

    # Translates 1D index to 2D index
    @staticmethod
    def oneDToTwoD(n, width=3, heigth=3):
        return n % width, n // heigth

    # Function to write to a field
    def writeField(self, input, x, y=None):
        n = x if y is None else self.twoDToOneD(x, y)
        self.fields[n] = input

    # Check whether x is within the allowable range
    def isWithinBoard(self, x, y=None):
        if y is None:
            return (0 <= x < len(self.fields))
        else:
            return 0 <= x < 3 and 0 <= y < 3

    # Check whether the location of the input is already taken
    def isFieldFree(self, x, y=None):
        n = x if y is None else self.twoDToOneD(x, y)
        return self.fields[n] is -1

    # Check whether the current field is a win
    def isWin(self, sign, x, y=None):
        n = x if y is None else self.twoDToOneD(x, y)

        # Checking in a horizontal line
        def horizontalWin(n, sign):
            # Check if all values are equal the played sign
            test = self.row(n)
            return all(f == sign for f in test)

        # Checking in a vertical line.
        def verticalWin(n, sign):
            # Check if all values are equal the played sign
            test = self.column(n)
            return all(f == sign for f in test)

        # Checking in a downward diagonal line.
        # i=0 is downward, i=1 is upward
        def diagonalWin(sign, i):
            # Check if all values are equal the played sign
            test = self.diagonal(i)
            return all(f == sign for f in test)

        # Every field can have a vertical/horizontal win, so just
        # save the value
        verHoriWin = verticalWin(n, sign) or horizontalWin(n, sign)

        # Check win condition.
        if n == 0 or n == 8:  # Upper left and lower right corner
            return verHoriWin or diagonalWin(sign, 0)
        elif n == 2 or n == 6:  # Upper right and lower left corner
            return verHoriWin or diagonalWin(sign, 1)
        if n == 4:  # Center
            return verHoriWin or diagonalWin(sign, 0) or diagonalWin(sign, 1)
        else:  # Edges
            return verHoriWin

    # Check whether the current board is in a draw state
    def isDraw(self):
        return len(self.freeFields()) == 0


if __name__ == "__main__":
    b = Board()
    b.fields = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    b.printExampleBoard(1)
    print()
    b.printExampleBoard()
