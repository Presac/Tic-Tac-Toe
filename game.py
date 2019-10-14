
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
            return 0 <= int(y) < len(self.fields)
        return False

    # Check whether x is within the allowable range
    def withinX(self, x):
        if x.isdigit():
            return 0 <= int(x) < len(self.fields[0])
        return False

    # Check whether the location of the input is already taken
    def fieldFree(self, x, y, input):
        return self.fields[y][x] is False


def game():
    board = Board()
    board.printBoard()

    print('Player')

    # Main game run
    while True:

        # Request the player to input which field to use
        while True:
            print('Choose row')
            y = getInput(board.withinY)
            print('Choose coloumn')
            x = getInput(board.withinX)

            # Check if field is already free
            if board.fieldFree(x, y, 'X'):
                board.writeField(x, y, 'X')
                break
            else:
                print('The field is already taken. Please choose a new one.')

        board.printBoard()


# Returns a value from an input within the requirements of a function func
def getInput(func):
    val = input()
    if not func(val):
        while not func(val):
            print('Please choose a number within the range of the board')
            val = input()
    return int(val)


if __name__ == "__main__":
    game()
