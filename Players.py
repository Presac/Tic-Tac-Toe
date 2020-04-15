from random import randint, choice
from collections import Counter
from Board import Board


# Player class for saving name and which sign to use
class Player():
    def __init__(self, name, sign):
        """
        Initialize a human player

        :param name: the name of the player
        :param sign: the sign the player plays with
        """
        self.name = name
        self.sign = sign
        self.type = 'human'

    # Asks for and returns a 2 part value from an input
    def getInput(self, board):
        """
        Get the input for a human player

        :param board: the board to play on
        """
        # while True:
        #     print('Choose row and coloumn (col row): ', end='')
        #     # Try for input, in case the user doesn't input two values
        #     try:
        #         x, y = input().split(' ')
        #     except ValueError:
        #         print('Input is not 2 values.')
        #         continue

        #     # Check if any of the two values is not an int
        #     if not (x.isdigit() and y.isdigit()):
        #         print('Input is not a number. Letters won\'t work.')
        #         continue

        #     # Check if the values confine to the board
        #     if board.isWithinBoard(int(x) - 1, int(y) - 1):
        #         break

        #     print('The choice is not within the range of the board.')

        # return board.twoDToOneD(int(x) - 1, int(y) - 1)

        while True:
            print('Choose a field: ', end='')
            x = input()

            # Check if any of the two values is not an int
            if not x.isdigit():
                print('Input is not a number. Letters won\'t work.')
                continue

            # Check if the values confine to the board
            if board.isWithinBoard(int(x) - 1):
                break

            print('The choice is not within the range of the board.')

        return int(x) - 1

    def getCharacter(self, board):
        return board.getCharacter(self.sign)


# AI inherits from player
class AI(Player):
    def __init__(self, name, sign, difficulty):
        """
        Initialize a ai player

        :param name: the name of the player
        :param sign: the sign the ai plays with
        :param difficulty: the difficulty the ai should play at
        """
        super().__init__(name, sign)
        # Will be used when different difficulties are made
        self.difficulty = int(difficulty)
        self.type = 'ai'

    # Get input depending on difficulty
    def getInput(self, board):
        """
        Get an input depending on the difficulty
        """
        if self.difficulty == 0:
            return self.chooseRandom(board)
        elif self.difficulty == 1:
            return self.smart(board)
        else:
            return self.chooseFuture(board)

    # Choose a random free field
    def chooseRandom(self, board):
        """
        Choose a random value from a number of free fields from the board

        :param board: the board to choose the free fields from
        :returns: an int
        """
        free = board.freeFields()
        if len(free) > 0:
            i = randint(0, len(free) - 1)
        else:
            return None

        return free[i]

    # Choose a free field depending on what is already taken
    def smart(self, board):
        """
        A "smart" ai to choose between the available fields depending on the
        threat level of each field.

        :param board: the board to choose a field from
        :returns: an int
        """
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

        # Get a list with all the win fields
        win = [state['n'] for state in states if state['win'] is True]
        if len(win) > 0:
            # No need to go further, as this will finish the game
            return choice(win)

        # Get a list with all the loss fields
        lose = [state['n'] for state in states if state['lose'] is True]
        if len(lose) > 0:
            # No need to go further. Not choosing the field will end the game
            return choice(lose)

        # Get a list with all the threat fields (towards the player)
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
        """
        Checks the state of list

        :param line: a list
        :returns: a list of the different states the line has
        """
        state = {'win': False, 'lose': False, 'threat': 0}
        lineSet = set(line)
        # full or empty
        if len(lineSet) == 1:
            pass  # None
        if len(lineSet) == 2:
            # Count the number of empty fields
            # Either a win or a possible loss
            if line.count(0) == 1:
                state['win'] = self.sign in line
                state['lose'] = self.sign not in line
            # A threat can be made
            if self.sign in line and line.count(0) == 2:
                state['threat'] = 1
        return state

    def chooseFuture(self, board):

        self.total = 0
        def max_value(fields):
            self.total += 1
            if board.isTerminal(fields):
                return board.utilityOf(fields, self.sign)
            v = -infinity
            for (a, s) in board.successorsOf(fields):
                v = max(v, min_value(s))
            return v

        def min_value(fields):
            self.total += 1
            if board.isTerminal(fields):
                return board.utilityOf(fields, self.sign)
            v = infinity
            for (a, s) in board.successorsOf(fields):
                v = min(v, max_value(s))
            return v

        def argmax(iterable, func):
            return max(iterable, key=func)

        infinity = float('inf')
        fields = board.fields[:]
        action, fields = argmax(board.successorsOf(fields), lambda a: min_value(a[1]))
        print(f'Total amount of runs: {self.total}')
        return action


    @staticmethod
    def merge_dicts(x, y):
        """
        Returns a merge of two dictionaries. The values need to be either
        Bool or numbers
        
        :param x: the first dictionary
        :param y: the second dictionary
        :returns: a dictionary
        """
        z = {}
        for k, v in x.items():
            z[k] = v or y[k] if type(v) is bool else v + y[k]
        return z
