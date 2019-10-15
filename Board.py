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
    def freeFields(self):
        free = []
        for i, field in enumerate(self.fields):
            if field is -1:
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
    def twoDToOneD(self, x, y):
        return x + y*3

    # Translates 1D index to 2D index
    def oneDToTwoD(self, n):
        return n % 3, n // 3

    # Function to write to a field
    def writeField(self, x, y, input):
        self.fields[self.twoDToOneD(x, y)] = input

    # region
    """
    # Check whether y is within the allowable range
    def isWithinY(self, y):
        return 0 <= int(y) - 1 < len(self.fields)

    # Check whether x is within the allowable range
    def isWithinX(self, x):
        return 0 <= int(x) - 1 < len(self.fields[0])
        """
    # endregion

    # Check whether x is within the allowable range
    def isWithinBoard(self, x, y):
        return (0 <= self.twoDToOneD(x, y) < len(self.fields))

    # Check whether the location of the input is already taken
    def isFieldFree(self, x, y):
        return self.fields[self.twoDToOneD(x, y)] is -1

    # Check whether the current field is a win
    def isWin(self, x, y, sign):
        n = self.twoDToOneD(x, y)

        # Functions to check for sign in each form of line

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

        # Check if input field is in a corner
        # Corners are 0, 2, 6 and 8, thus the following check
        if n % 2 == 0 and n != 4:
            if n == 0 or n == 8:
                temp = diagonalWin(sign, 0)
            else:
                temp = diagonalWin(sign, 1)
            return verticalWin(n, sign) or horizontalWin(n, sign) or temp

        # Check if input field is in the center
        if n == 4:
            return verticalWin(n, sign) or horizontalWin(n, sign) or \
                diagonalWin(sign, 0) or diagonalWin(sign, 1)

        # Check if input field is at the edge
        # Edges are 1, 3, 5, 7, thus the following
        if n % 2 == 1:
            return verticalWin(n, sign) or horizontalWin(n, sign)

    # Check whether the current board is in a draw state
    def isDraw(self):
        return len(self.freeFields()) == 0


if __name__ == "__main__":
    b = Board()
    b.fields = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    b.printExampleBoard(1)
    b.printExampleBoard()
    print(b.diagonal(1))
