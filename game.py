from random import randint, choice
from Board import Board
# from collections import Counter


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
            if board.isWithinBoard(int(x) - 1, int(y) - 1):
                break

            print('The choice is not within the range of the board.')

        return board.twoDToOneD(int(x) - 1, int(y) - 1)


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

        return free[i]

    # Choose a free field depending on what is already taken
    def chooseSmart(self, board):
        # Stores fields which will make the AI win if taken
        winFields = []
        # Stores fields which will make the AI lose if not taken
        loseFields = []
        # Stores fields which can make a threat to the opponent
        threatFields = []

        # Go through each row/column
        for n in range(0, 9, 4):
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
                winFields.append(board.twoDToOneD(row.index(-1), n % 3))
            # For column
            if len(colSet) == 2 and self.sign in colSet and -1 in colSet \
                    and col.count(self.sign) == 2:
                winFields.append(board.twoDToOneD(n % 3, col.index(-1)))

            # Check if the opponents sign is twice in the row/column
            # and one free field is available = Loss
            # For row
            if len(rowSet) == 2 and self.sign not in rowSet and -1 in rowSet \
                    and row.count(-1) == 1:
                loseFields.append(board.twoDToOneD(row.index(-1), n % 3))
            # For column
            if len(colSet) == 2 and self.sign not in colSet and -1 in colSet \
                    and col.count(-1) == 1:
                loseFields.append(board.twoDToOneD(n % 3, col.index(-1)))

            # Check if there are fields that can make a threat to the opponent
            # For row
            if len(rowSet) == 2 and self.sign in rowSet and row.count(-1) == 2:
                for i in range(3):
                    if row[i] == -1:
                        threatFields.append(board.twoDToOneD(i, n % 3))
            # For column
            if len(colSet) == 2 and self.sign in colSet and col.count(-1) == 2:
                for i in range(3):
                    if col[i] == -1:
                        threatFields.append(board.twoDToOneD(n % 3, i))

        # Do the same for the two diagonal lines
        for n in range(2):
            dia = board.diagonal(n)
            diaSet = set(dia)

            # Check if the ai's sign is twice in the row/column
            # and one free field is available = Win
            if len(diaSet) == 2 and self.sign in diaSet and -1 in diaSet \
                    and dia.count(-1) == 1:
                col = dia.index(-1)
                winFields.append(board.twoDToOneD(col, 2*n - 2*n*col + col))

            # Check if the opponents sign is twice in the row/column
            # and one free field is available = Loss
            if len(diaSet) == 2 and self.sign not in diaSet and -1 in diaSet \
                    and dia.count(-1) == 1:
                col = dia.index(-1)
                loseFields.append(board.twoDToOneD(col, 2*n - 2*n*col + col))

            # Check if the ai's sign is in the row/column
            # and two free fields is available
            if len(diaSet) == 2 and self.sign in diaSet and dia.count(-1) == 2:
                for i in range(3):
                    if dia[i] == -1:
                        threatFields.append(
                            board.twoDToOneD(i, 2*n - 2*n*i + i))

        # If any field can give a win, choose one at random
        if len(winFields) > 0:
            i = choice(winFields)
            return i

        # If any field is about to make it lose, choose one at random
        if len(loseFields) > 0:
            i = choice(loseFields)
            return i

        if len(threatFields) > 0:
            # TODO prioritise threatFields that occurs the most
            # ttf = dict([(k, v) for k, v in enumerate(threatFields)])
            # ctr = Counter(ttf.values())
            i = choice(threatFields)
            return i

        # If no win or lose fields are available and no threats can be made,
        # choose at random
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
        print(f'{players[player].name} ({board.signs[players[player].sign]})'
              'is having their turn.')
        # Request the player to input which field to use
        while True:
            n = players[player].getInput(board)

            # Check if field is already free
            if board.isFieldFree(n):
                board.writeField(players[player].sign, n)
                break
            else:
                print('The field is already taken.'
                      'Please choose a new one.')

        board.printBoard()

        # Check if the player has won
        if board.isWin(players[player].sign, n):
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
