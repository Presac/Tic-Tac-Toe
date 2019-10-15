# Board class containing the state of the board and commands pertaining to it
class Board:
    # Either 1 or 2
    signs = ('X', 'O')

    def __init__(self):
        # Represents 9 fields
        self.fields = [[-1 for x in range(3)] for y in range(3)]

    # Reset the board to the inital state
    def resetBoard(self):
        self.fields = [[-1 for x in range(3)] for y in range(3)]

    # Prints the board with 3 fields in each line
    def printBoard(self):
        fieldStr = ''
        for y in range(len(self.fields)):
            for x in range(len(self.fields[y])):
                if self.fields[y][x] is -1:
                    fieldStr += '[   ]'
                else:
                    fieldStr += f'[ {self.signs[self.fields[y][x]]} ]'
            fieldStr += '\n'
        print(fieldStr)

    # Prints an example board with the index of each field
    def printExampleBoard(self):
        fieldStr = ''
        for y in range(len(self.fields)):
            for x in range(len(self.fields[y])):
                fieldStr += f'[{x+1} {y+1}]'
            fieldStr += '\n'
        print(fieldStr)

    # Returns a list of all free fields
    def freeFields(self):
        free = []
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                if field is -1:
                    free.append([j, i])
        return free

    # Returns n'th row
    def row(self, n):
        return self.fields[n]

    # Returns n'th column
    def column(self, n):
        return [self.fields[i][n] for i in range(3)]

    # Returns one of the two diagonals
    # n=0 is a downward diagonal, n=1 an upward diagonal
    def diagonal(self, n):
        # The formula ensures the direction of the slope
        return [self.fields[2*n - 2*n*i + i][i] for i in range(3)]

    # Function to write to a field
    def writeField(self, x, y, input):
        self.fields[y][x] = input

    # Check whether x is within the allowable range
    def isWithinBoard(self, x, y):
        return (0 <= x - 1 < len(self.fields[0])) and \
            (0 <= y - 1 < len(self.fields))

    # Check whether the location of the input is already taken
    def isFieldFree(self, x, y):
        return self.fields[y][x] is -1

    # Check whether the current field is a win
    def isWin(self, x, y, sign):

        # Functions to check for sign in each form of line

        # Checking in a horizontal line
        def horizontal(y, sign):
            # Check if all values are equal the played sign
            return all(f == sign for f in self.fields[y])

        # Checking in a vertical line.
        def vertical(x, sign):
            # Check if all values are equal the played sign
            return all(f == sign for f in
                       [self.fields[i][x] for i in range(3)])

        # Checking in a downward diagonal line.
        def downDiagonal(sign):
            # Check if all values are equal the played sign
            return all(f == sign for f in
                       [self.fields[i][i] for i in range(3)])

        # Checking in a upward diagonal line.
        def upDiagonal(sign):
            # Check if all values are equal the played sign
            return all(f == sign for f in
                       [self.fields[2-i][i] for i in range(3)])

        # Check if input field is in a corner
        if (y == 0 or y == 2) and (x == 0 or x == 2):
            if x == y:
                temp = downDiagonal(sign)
            else:
                temp = upDiagonal(sign)
            return vertical(x, sign) or horizontal(y, sign) or temp

        # Check if input field is in the center
        if y == 1 and x == 1:
            return vertical(x, sign) or horizontal(y, sign) or \
                downDiagonal(sign) or upDiagonal(sign)

        # Check if input field is at the edge
        if (y == 1 and (x == 0 or x == 2)) or (x == 1 and (y == 0 or y == 2)):
            return vertical(x, sign) or horizontal(y, sign)

    # Check whether the current board is in a draw state
    def isDraw(self):
        return len(self.freeFields()) == 0
