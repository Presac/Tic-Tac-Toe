from random import randint, choice
from collections import Counter
from Board import Board


# Player class for saving name and which sign to use
class Player():
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign
        self.type = 'human'

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
        self.difficulty = int(difficulty)
        self.type = 'ai'

    # Get input depending on difficulty
    def getInput(self, board):
        if self.difficulty != 0:
            return self.smart2(board)
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

            # For row
            if len(rowSet) == 2 and self.sign in row and row.count(-1) == 1:
                winFields.append(Board.twoDToOneD(row.index(-1), n % 3))
            # For column
            if len(colSet) == 2 and self.sign in col and col.count(-1) == 1:
                winFields.append(Board.twoDToOneD(n % 3, col.index(-1)))

            # Check if the opponents sign is twice in the row/column
            # and one free field is available = Loss
            # For row
            if len(rowSet) == 2 and self.sign not in rowSet \
                    and row.count(-1) == 1:
                loseFields.append(Board.twoDToOneD(row.index(-1), n % 3))
            # For column
            if len(colSet) == 2 and self.sign not in col and -1 in colSet \
                    and col.count(-1) == 1:
                loseFields.append(Board.twoDToOneD(n % 3, col.index(-1)))

            # Check if there are fields that can make a threat to the opponent
            # For row
            if len(rowSet) == 2 and self.sign in row and row.count(-1) == 2:
                for i in range(3):
                    if row[i] == -1:
                        threatFields.append(Board.twoDToOneD(i, n % 3))
            # For column
            if len(colSet) == 2 and self.sign in col and col.count(-1) == 2:
                for i in range(3):
                    if col[i] == -1:
                        threatFields.append(Board.twoDToOneD(n % 3, i))

        # Do the same for the two diagonal lines
        for n in range(2):
            dia = board.diagonal(n)
            diaSet = set(dia)

            # Check if the ai's sign is twice in the row/column
            # and one free field is available = Win
            if len(diaSet) == 2 and self.sign in dia and dia.count(-1) == 1:
                col = dia.index(-1)
                winFields.append(Board.twoDToOneD(col, 2*n - 2*n*col + col))

            # Check if the opponents sign is twice in the row/column
            # and one free field is available = Loss
            if len(diaSet) == 2 and self.sign not in dia and \
                    dia.count(-1) == 1:
                col = dia.index(-1)
                loseFields.append(Board.twoDToOneD(col, 2*n - 2*n*col + col))

            # Check if the ai's sign is in the row/column
            # and two free fields is available
            if len(diaSet) == 2 and self.sign in dia and dia.count(-1) == 2:
                for i in range(3):
                    if dia[i] == -1:
                        threatFields.append(
                            Board.twoDToOneD(i, 2*n - 2*n*i + i))

        # If any field can give a win, choose one at random
        if len(winFields) > 0:
            i = choice(winFields)
            return i

        # If any field is about to make it lose, choose one at random
        if len(loseFields) > 0:
            i = choice(loseFields)
            return i

        if len(threatFields) > 0:
            # Prioritise threatFields that occurs the most
            ctr = Counter(threatFields).most_common()
            highest = []
            most = -1
            for k, v in ctr:
                if v >= most:
                    most = v
                    highest.append(k)
                else:
                    break
            i = choice(highest)
            return i

        # If no win or lose fields are available and no threats can be made,
        # choose at random
        return self.chooseRandom(board)

    def smart2(self, board):
        free = board.freeFields()
        states = []

        # Check each free field for their state
        for n in free:
            # Get the diagonal lines
            diagonal = [board.diagonal(0), board.diagonal(1)]

            # Get the state of the fields row and column
            # As every field has them, they will always be checked
            state = self.merge_dicts(self.checkLine(board.row(n)),
                                     self.checkLine(board.column(n)))

            # Check if the field is in one of the diagonals
            if n == 0 or n == 8:  # Upper left and lower right corner
                state = self.merge_dicts(state, self.checkLine(diagonal[0]))
            elif n == 2 or n == 6:  # Upper right and lower left corner
                state = self.merge_dicts(state, self.checkLine(diagonal[1]))
            if n == 4:  # Center
                state = self.merge_dicts(state, self.checkLine(diagonal[0]))
                state = self.merge_dicts(state, self.checkLine(diagonal[1]))

            # Save the field number in state together with
            # the state of the field
            states.append({**{'n': n}, **state})

        # Get a list with all the win/loss/threat fields
        win = [state['n'] for state in states if state['win'] is True]
        if len(win) > 0:
            # No need to go further, as this will finish the game
            return choice(win)

        lose = [state['n'] for state in states if state['lose'] is True]
        if len(lose) > 0:
            # No need to go further. Not choosing the field will end the game
            return choice(lose)

        threats = {state['n']: state['threat']
                   for state in states if state['threat'] != 0}
        if len(threats) > 0:
            # Sort by order of highest threat
            ctr = Counter(threats).most_common()
            # Get the fields with the highest threat
            maxes = [k for k, v in ctr if v == ctr[0][1]]
            return choice(maxes)
        return self.chooseRandom(board)

    def checkLine(self, line):
        state = {'win': False, 'lose': False, 'threat': 0}
        lineSet = set(line)
        # full or empty
        if len(lineSet) == 1:
            pass  # None
        if len(lineSet) == 2:
            # Either a win or a possible loss
            if line.count(-1) == 1:
                state['win'] = self.sign in line
                state['lose'] = self.sign not in line
            # A threat can be made
            if self.sign in line and line.count(-1) == 2:
                state['threat'] = 1
        return state

    @staticmethod
    def merge_dicts(x, y):
        '''Returns a merge of two dictionaries. The values need to be either
        Bool or numbers'''
        z = {}
        for k, v in x.items():
            z[k] = v or y[k] if type(v) is bool else v + y[k]
        return z
