from Board import Board
from Players import Player, AI
from gui import Application
import tkinter as tk
import argparse


def game():
    """
    The top level game loop.
    Gets the players and resets the game board at the start of each game then
    starts the main game loop
    """
    board = Board()
    print('Welcome to a game of Tic-Tac-Toe')
    while True:
        players = chooseGamemode()

        if players is None:
            continue
        elif players is 'End':
            break

        board.resetBoard()
        runGame(board, players)

def chooseGamemode():
    """
    Function to choose the game mode and difficulty.

    :returns: A list of the two players, either ai or player.
    """

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
        return 'End'
    elif val == '1':
        player1 = Player('Player 1', -1)
        player2 = Player('Player 2', 1)
    elif val == '2':
        print('Which difficulty do you want to play against?\n'
                '0: Easy.\n'
                '1: Hard.')
        difficulty = input('(default: 0): ')

        if difficulty not in ['0', '1']:
            difficulty = '0'
            print('Defaultet to 0: Easy')
        
        print()

        player1 = Player('Player 1', -1)
        player2 = AI('AI', 1, difficulty)
    elif val == '3':
        player1 = AI('Smart AI', -1, '1')
        player2 = AI('Stupid AI', 1, '0')
    elif val == '4':
        player1 = AI('Stupid AI 1', -1, '0')
        player2 = AI('Smart AI 2', 1, '1')
    elif val == '5':
        player1 = AI('Smart AI 1', -1, '1')
        player2 = AI('Smart AI 2', 1, '1')
    else:
        print('Not an option.')
        return None

    return [player1, player2]

def runGame(board, players):
    """
    Handles the main game loop.

    :param board: the board to play the game on
    :param players: a list with two players, either ai or player.
    """
    print('The following board shows each fields index number.')
    board.printExampleBoard(True)

    currentP = toggleValue()

    # Main game run
    while True:
        player = next(currentP)
        print(f'\n{players[player].name} ({players[player].getCharacter(board)}) '
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
    parser = argparse.ArgumentParser(description='A tic-tac-toe game.')
    parser.add_argument('-m', '--mode', nargs='?', default='gui')

    args = parser.parse_args()
    
    if args.mode == 'cmd':
        game()
    else:
        root = tk.Tk()
        app = Application(master=root)
        app.mainloop()
