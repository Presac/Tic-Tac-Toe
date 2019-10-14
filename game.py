
class Board:
    # Either 1 or 2
    signs = ('X', 'O')

    def __init__(self):
        # Represents 9 fields
        self.fields = [[-1 for x in range(3)] for y in range(3)]

    # Reset the board to the inital state
    def resetBoard(self):
        self.fields = [[-1 for x in range(3)] for y in range(3)]

    # Prints the table with 3 fields in each line
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

    # Function to write to a field
    def writeField(self, x, y, input):
        self.fields[y][x] = input

    # Check whether y is within the allowable range
    def withinY(self, y):
        return 0 <= int(y) - 1 < len(self.fields)

    # Check whether x is within the allowable range
    def withinX(self, x):
        return 0 <= int(x) - 1 < len(self.fields[0])

    # Check whether x is within the allowable range
    def withinBoard(self, x, y):
        return (0 <= int(x) - 1 < len(self.fields[0])) and \
            (0 <= int(y) - 1 < len(self.fields))

    # Check whether the location of the input is already taken
    def fieldFree(self, x, y):
        return self.fields[y][x] is -1

    # Check whether the current field is a win
    def isWin(self, x, y, sign):

        # Functions to check for sign in each form of line

        # Checking in a horizontal line
        def horizontal(y, sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in self.fields[y]):
                return True
            return False

        # Checking in a vertical line.
        def vertical(x, sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in [self.fields[i][x] for i in range(3)]):
                return True
            return False

        # Checking in a downward diagonal line.
        def downDiagonal(sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in [self.fields[i][i] for i in range(3)]):
                return True
            return False

        # Checking in a upward diagonal line.
        def upDiagonal(sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in [self.fields[2-i][i] for i in range(3)]):
                return True
            return False

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


# Player class for saving name and which sign to use
class Player():
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign


def game():
    while True:
        board = Board()
        board.printBoard()

        player1 = Player('Player 1', 0)
        player2 = Player('Player 2', 1)

        players = [player1, player2]
        currentP = toggleValue()

        # Main game run
        while True:
            player = next(currentP)
            print(f'{players[player].name} is having their turn.')
            # Request the player to input which field to use
            while True:
                x, y = getInput(board.withinBoard)

                # Check if field is already free
                if board.fieldFree(x, y):
                    board.writeField(x, y, players[player].sign)
                    break
                else:
                    print('The field is already taken.'
                          'Please choose a new one.')

            board.printBoard()

            # Check if the player has won
            if board.isWin(x, y, players[player].sign):
                print(f'{players[player].name} has won the game.')
                # Stop current game
                break

        print('Do you want to play again (Y/N)? ')
        val = input('(Default Y): ')
        if val.lower() == 'n':
            print('Thanks for playing :)')
            break


# Asks for and returns a value from an input within the requirements of a
# function func
def getInput(func):
    while True:
        print('Choose row and coloumn (col row): ', end='')
        # Try for input, in case the user doesn't input two values
        try:
            x, y = input().split(' ')
        except ValueError:
            print('Input is not 2 values.')
            continue

        # Check if any of the two values is not an int
        if not (x.isdigit() and y.isdigit()):
            print('Input is not a number. Letters won\'t work.')
            continue

        # Check if the values confine within the restrictions of a func
        if func(x, y):
            break

        print('The choice is not within the range of the board.')

    return int(x) - 1, int(y) - 1


# Iterator for going between 0 and 1
def toggleValue():
    while True:
        yield 0
        yield 1


if __name__ == "__main__":
    game()
