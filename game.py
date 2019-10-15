from random import randint, choice


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
        return len(self.freeFields()) == 0


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
    def __init__(self, name, sign, difficulty):
        super().__init__(name, sign)
        # Will be used when different difficulties are made
        self.difficulty = difficulty

    # Get input depending on difficulty
    def getInput(self, board):
        if self.difficulty != '0':
            return self.chooseSmart(board)
        else:
            return self.chooseRandom(board)

    # Choose a random free field
    def chooseRandom(self, board):
        free = board.freeFields()
        i = randint(0, len(free) - 1)

        return free[i][0], free[i][1]

    # Choose a free field depending on what is already taken
    def chooseSmart(self, board):
        # Stores fields which will make the AI win if taken
        winFields = []
        # Stores fields which will make the AI lose if not taken
        loseFields = []

        # Check if the ai can put its third sign in a line
        for n in range(3):
            # Get the row/column and save it as set to remove dupes
            row = board.row(n)
            rowSet = set(row)
            col = board.column(n)
            colSet = set(col)

            # Check if the ai's sign is twice in the row/column
            # and one free field is available = Win
            # For row
            if len(rowSet) == 2 and self.sign in rowSet and -1 in rowSet \
                    and row.count(self.sign) == 2:
                winFields.append([row.index(-1), n])
            # For column
            if len(colSet) == 2 and self.sign in colSet and -1 in colSet \
                    and col.count(self.sign) == 2:
                winFields.append([n, col.index(-1)])

            # Check if the opponents sign is twice in the row/column
            # and one free field is available = Loss
            # For row
            if len(rowSet) == 2 and self.sign not in rowSet and -1 in rowSet \
                    and row.count(-1) == 1:
                loseFields.append([row.index(-1), n])
            # For column
            if len(colSet) == 2 and self.sign not in colSet and -1 in colSet \
                    and col.count(-1) == 1:
                loseFields.append([n, col.index(-1)])

        # Do the same for the two diagonal lines
        for n in range(2):
            dia = board.diagonal(n)
            diaSet = set(dia)

            # Check if the ai's sign is twice in the row/column
            # and one free field is available = Win
            if len(diaSet) == 2 and self.sign in diaSet and -1 in diaSet \
                    and dia.count(-1) == 1:
                col = dia.index(-1)
                winFields.append([col, 2*n - 2*n*col + col])

            # Check if the opponents sign is twice in the row/column
            # and one free field is available = Loss
            if len(diaSet) == 2 and self.sign not in diaSet and -1 in diaSet \
                    and dia.count(-1) == 1:
                col = dia.index(-1)
                loseFields.append([col, 2*n - 2*n*col + col])

        # If any field can give a win, choose one at random
        if len(winFields) > 0:
            i = choice(winFields)
            return i[0], i[1]

        # If any field is about to make it lose, choose one at random
        if len(loseFields) > 0:
            i = choice(loseFields)
            return i[0], i[1]

        """ # Check if there are fields that can make a threat to the opponent
        threatFields = []
        # Check if there can be made a to tile thread
        for n in range(3):
            row = board.row(n)
            rowSet = set(row)
            col = board.column(n)
            colSet = set(col)

            # For row
            if len(rowSet) == 2 and self.sign in rowSet and row.count(-1) == 2:
                threatFields.append([row.index(-1), n])
            # For column
            if len(colSet) == 2 and self.sign in colSet and col.count(-1) == 2:
                threatFields.append([n, col.index(-1)])

        for n in range(2):
            dia = board.diagonal(n)
            diaSet = set(dia)

            # Check if the ai's sign is twice in the row/column
            # and one free field is available
            if len(diaSet) == 2 and self.sign in diaSet and dia.count(-1) == 2:
                col = dia.index(-1)
                threatFields.append([col, 2*n - 2*n*col + col])

        if len(threatFields) > 0:
            i = choice(threatFields)
            return i[0], i[1] """

        # If no win or lose fields are available, choose at random
        return self.chooseRandom(board)


def game():
    board = Board()
    print('Welcome to a game of Tic-Tac-Toe')
    while True:
        print('What do you want to do? Pick from the options below.\n'
              '1: Play against another player.\n'
              '2: Play against the computer.\n'
              '3: Smart (starting) against stupid computer.\n'
              '4: Stupid (starting) against Smart computer.\n'
              '5: Smart against smart computer.\n'
              '0: Exit')
        val = input('Choose an option: ')
        print()

        if val == '0':
            print('Hope to see you again :)')
            break
        elif val == '1':
            player1 = Player('Player 1', 0)
            player2 = Player('Player 2', 1)

            players = [player1, player2]
        elif val == '2':
            print('Which difficulty do you want to play against?\n'
                  '0: Very easy.\n'
                  '1: Very hard.')
            difficulty = input('(default: 0): ')
            print()

            player1 = Player('Player 1', 0)
            player2 = AI('AI', 1, difficulty)

            players = [player1, player2]
        elif val == '3':
            player1 = AI('Smart AI', 0, '1')
            player2 = AI('Stupid AI', 1, '0')

            players = [player1, player2]
        elif val == '4':
            player1 = AI('Stupid AI 1', 0, '0')
            player2 = AI('Smart AI 2', 1, '1')

            players = [player1, player2]
        elif val == '5':
            player1 = AI('Smart AI 1', 0, '1')
            player2 = AI('Smart AI 2', 1, '1')

            players = [player1, player2]
        else:
            print('Not an option.')
            continue

        while True:
            board.resetBoard()
            runGame(board, players)
            break


def runGame(board, players):
    print('The following board shows each fields index number.')
    board.printExampleBoard()

    currentP = toggleValue()

    # Main game run
    while True:
        player = next(currentP)
        print(f'{players[player].name} ({board.signs[players[player].sign]}) is having their turn.')
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
            print(f'{players[player].name} has won the game.\n')
            # Stop current game
            break

        # Check if no more fields are free
        if board.isDraw():
            print('The game has ended in a draw.\n')
            # Stop current game
            break


# Iterator for going between 0 and 1
def toggleValue():
    while True:
        yield 0
        yield 1


if __name__ == "__main__":
    game()
