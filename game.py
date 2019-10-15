from random import randint


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

    def freeFields(self):
        free = []
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                if field is -1:
                    free.append([j, i])
        return free

    # Function to write to a field
    def writeField(self, x, y, input):
        self.fields[y][x] = input

    # Check whether y is within the allowable range
    def isWithinY(self, y):
        return 0 <= int(y) - 1 < len(self.fields)

    # Check whether x is within the allowable range
    def isWithinX(self, x):
        return 0 <= int(x) - 1 < len(self.fields[0])

    # Check whether x is within the allowable range
    def isWithinBoard(self, x, y):
        return (0 <= int(x) - 1 < len(self.fields[0])) and \
            (0 <= int(y) - 1 < len(self.fields))

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
        return len(self.freeFields()) is 0


# Player class for saving name and which sign to use
class Player():
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign

    # Asks for and returns a 2 part value from an input
    def getInput(self, board):
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

            # Check if the values confine to the board
            if board.isWithinBoard(x, y):
                break

            print('The choice is not within the range of the board.')

        return int(x) - 1, int(y) - 1


# AI inherits from player
class AI(Player):
    # Returns a random field from within the free ones
    def getInput(self, board):
        free = board.freeFields()
        choice = randint(0, len(free) - 1)

        return free[choice][0], free[choice][1]


def game():
    board = Board()
    print('Welcome to a game of Tic-Tac-Toe')
    while True:
        print('What do you want to do?\n'
              '1: Play against another player.\n'
              '2: Play against the computer.\n'
              '3: Exit')
        val = input('Pick a number: ')
        if val == '1':
            player1 = Player('Player 1', 0)
            player2 = Player('Player 2', 1)

            players = [player1, player2]
        elif val == '2':
            player1 = Player('Player 1', 0)
            player2 = AI('AI', 1)

            players = [player1, player2]
        elif val == '3':
            print('Hope to see you again :)')
            break
        else:
            print('Not an option.')
            continue

        while True:
            board.resetBoard()
            runGame(board, players)
            break


def runGame(board, players):
    board.printBoard()

    currentP = toggleValue()

    # Main game run
    while True:
        player = next(currentP)
        print(f'{players[player].name} is having their turn.')
        # Request the player to input which field to use
        while True:
            x, y = players[player].getInput(board)

            # Check if field is already free
            if board.isFieldFree(x, y):
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

        # Check if no more fields are free
        if board.isDraw():
            print('The game has ended in a draw.')
            # Stop current game
            break


# Iterator for going between 0 and 1
def toggleValue():
    while True:
        yield 0
        yield 1


if __name__ == "__main__":
    game()
