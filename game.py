
class Board:
    # Represents 9 fields
    fields = [[False for x in range(3)] for y in range(3)]

    # Either 1 or 2
    player = False

    def __init__(self):
        pass

    # Prints the table with 3 fields in each line
    def printBoard(self):
        fieldStr = ''
        for y in range(len(self.fields)):
            for x in range(len(self.fields[y])):
                if not self.fields[y][x]:
                    fieldStr += '[   ]'
                else:
                    fieldStr += f'[ {self.fields[y][x]} ]'
            fieldStr += '\n'
        print(fieldStr)

    # Function to write to a field
    def writeField(self, x, y, input):
        self.fields[y][x] = input

    # Check whether y is within the allowable range
    def withinY(self, y):
        if y.isdigit():
            return 0 <= int(y) - 1 < len(self.fields)
        return False

    # Check whether x is within the allowable range
    def withinX(self, x):
        if x.isdigit():
            return 0 <= int(x) - 1 < len(self.fields[0])
        return False

    # Check whether the location of the input is already taken
    def fieldFree(self, x, y):
        return self.fields[y][x] is False

    def isWin(self, x, y, sign):

        # Functions to check for sign in each form of line

        # Checking in a horizontal line
        def horizontal(y, sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in self.fields[y]):
                return True
            else:
                return False

        # Checking in a vertical line.
        def vertical(x, sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in [self.fields[i][x] for i in range(3)]):
                return True
            else:
                return False

        # Checking in a downward diagonal line.
        def downDiagonal(sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in [self.fields[i][i] for i in range(3)]):
                return True
            else:
                return False

        # Checking in a upward diagonal line.
        def upDiagonal(sign):
            # Check if all values are equal the played sign
            if all(f == sign for f in [self.fields[2-i][i] for i in range(3)]):
                return True
            else:
                return False

        # corner
        if (y == 0 or y == 2) and (x == 0 or x == 2):
            if x == y:
                temp = downDiagonal(sign)
            else:
                temp = upDiagonal(sign)
            return vertical(x, sign) or horizontal(y, sign) or temp

        # center
        if y == 1 and x == 1:
            return vertical(x, sign) or horizontal(y, sign) or \
                downDiagonal(sign) or upDiagonal(sign)

        # edge
        if (y == 1 and (x == 0 or x == 2)) or (x == 1 and (y == 0 or y == 2)):
            return vertical(x, sign) or horizontal(y, sign)


# Player class for saving name and which sign to use
class Player():
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign


def game():
    board = Board()
    board.printBoard()

    player1 = Player('Player 1', 'X')
    player2 = Player('Player 2', 'O')

    players = [player1, player2]
    currentP = currentPlayer()

    # Main game run
    while True:
        player = next(currentP)
        print(f'{players[player].name} is having their turn.')
        # Request the player to input which field to use
        while True:
            print('Choose row: ', end='')
            y = getInput(board.withinY)
            print('Choose coloumn: ', end='')
            x = getInput(board.withinX)

            # Check if field is already free
            if board.fieldFree(x, y):
                board.writeField(x, y, players[player].sign)
                break
            else:
                print('The field is already taken. Please choose a new one.')

        board.printBoard()

        # Check if the player has won
        if board.isWin(x, y, players[player].sign):
            print(f'{players[player].name} has won the game.')
            # Stop current game
            break


# Returns a value from an input within the requirements of a function func
def getInput(func):
    val = input()
    if not func(val):
        while not func(val):
            print('Please choose a number within the range of the board')
            val = input()
    return int(val) - 1


# Iterator for going between 0 and 1
def currentPlayer():
    while True:
        yield 0
        yield 1


if __name__ == "__main__":
    game()
