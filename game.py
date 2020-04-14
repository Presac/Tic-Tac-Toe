from Board import Board
from Players import Player, AI

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
        elif val == '2':
            print('Which difficulty do you want to play against?\n'
                  '0: Very easy.\n'
                  '1: Very hard.')
            difficulty = input('(default: 0): ')
            print()

            player1 = Player('Player 1', 0)
            player2 = AI('AI', 1, difficulty)
        elif val == '3':
            player1 = AI('Smart AI', 0, '1')
            player2 = AI('Stupid AI', 1, '0')
        elif val == '4':
            player1 = AI('Stupid AI 1', 0, '0')
            player2 = AI('Smart AI 2', 1, '1')
        elif val == '5':
            player1 = AI('Smart AI 1', 0, '1')
            player2 = AI('Smart AI 2', 1, '1')
        else:
            print('Not an option.')
            continue

        players = [player1, player2]

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
