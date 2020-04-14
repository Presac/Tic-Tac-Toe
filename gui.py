import tkinter as tk
from tkinter import messagebox
from functools import partial
from Board import Board
from Players import Player, AI

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # A list of the different game modes
        self.OPTIONS = {
            'Player VS Player': 1, 
            'Player VS AI': 2, 
            'Smart VS Stupid': 3, 
            'Stupid VS Smart': 4, 
            'Smart VS Smart': 5
        }

        # A list of the different difficulties
        self.DIFFICULTY = {
            'Easy': 0,
            'Hard': 1
        }

        self.label_list = []
        self.board = Board()
        self.current_player = 0
        self._loop = None

        self.master = master
        self.master.resizable(False, False)

        self.var_mode = tk.StringVar(self.master)
        self.var_mode.set('Player VS AI')

        self.var_diff = tk.StringVar(self.master)
        self.var_diff.set('Easy')

        self.master.title('Tic-Tac-Toe')

        self.master.rowconfigure(0, minsize=500, weight=1)
        self.master.columnconfigure(1, minsize=500, weight=1)

        self.fr_controls = tk.Frame(self.master, width=500, relief=tk.RAISED, bd=2)
        self.fr_gamearea = tk.Frame(self.master)
        self.fr_gamegrid = tk.Frame(self.fr_gamearea)

        self.fr_gamearea.rowconfigure(1, minsize=500, weight=1)
        self.fr_gamearea.columnconfigure(0, minsize=500, weight=1)

        # Buttons and dropdowns for the control area
        self.btn_start = tk.Button(
            self.fr_controls, width=18, text='Start Game', command=self.startGame)
        self.om_modes = tk.OptionMenu(
            self.fr_controls, self.var_mode, *self.OPTIONS.keys())
        self.om_difficulty = tk.OptionMenu(
            self.fr_controls, self.var_diff, *self.DIFFICULTY.keys())


        self.lbl_curr_player = tk.Label(self.fr_gamearea, text='Current player:')

        self.fr_controls.grid(row=0, column=0, sticky='ns')
        self.fr_gamearea.grid(row=0, column=1, sticky='nsew')
        self.fr_gamegrid.grid(row=1, column=0, sticky='nsew')
        
        self.lbl_curr_player.grid(row=0, column=0, sticky='w')
        self.btn_start.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.om_modes.grid(row=1, column=0, sticky='ew', padx=5)
        self.om_difficulty.grid(row=2, column=0, sticky='ew', padx=5)

    def createGameGrid(self, frame):
        """
        Generates a 3 times 3 grid of frames each with a label inside

        :param frame: the frame to generate the grid within
        """
        # Clear the list of grid squares
        self.label_list = []

        for i in range(3):
            frame.columnconfigure(i, weight=1, minsize=100)
            frame.rowconfigure(i, weight=1, minsize=100)

            for j in range(3):
                self.fr_grid = tk.Frame(
                    frame,
                    relief=tk.RAISED,
                    borderwidth=1
                    )
                self.fr_grid.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')

                label = tk.Label(self.fr_grid, text=f" ", font=('-weight bold', 60))
                label.pack(fill=tk.BOTH, expand=True)
                
                # Bind a command to the label, corresponding to the number in the grid
                label.bind('<Button-1>', partial(self.handle_click, j+(i*3)))

                self.label_list.append(label)
    
    def handle_click(self, number, event):
        """
        Handles the human players clicks.

        :param number: the grid number the player has clicked on.
        :param event: the event that triggered the command
        """
        # Ensure the field isn't taken yet and that it is only possible to click
        # when it is the players turn.
        if self.label_list[number]['text'] != ' ' or \
           self.players[self.current_player].type == 'ai':
            return
        
        ended = self.handle_step(number)

        # Disable the ability to click on the board when the game is finished
        if ended:
            for field in self.label_list:
                field.unbind('<Button-1>')
    
    def startGame(self):
        """
        Gets the mode and difficulty from the dropdown menues and sets the players.
        Starts the game loop to handle a possible ai.
        """
        mode = self.OPTIONS[self.var_mode.get()]
        diff = self.DIFFICULTY[self.var_diff.get()]

        if mode == 1:
            player1 = Player('Player 1', 0)
            player2 = Player('Player 2', 1)
        elif mode == 2:
            player1 = Player('Player 1', 0)
            player2 = AI('AI', 1, diff)
        elif mode == 3:
            player1 = AI('Smart AI', 0, 1)
            player2 = AI('Stupid AI', 1, 0)
        elif mode == 4:
            player1 = AI('Stupid AI 1', 0, 0)
            player2 = AI('Smart AI 2', 1, 1)
        else:  # mode == '5':
            player1 = AI('Smart AI 1', 0, 1)
            player2 = AI('Smart AI 2', 1, 1)

        # Reset the board state
        self.board.resetBoard()
        self.players = [player1, player2]
        self.player_iterator = self.toggleValue()

        self.current_player = next(self.player_iterator)

        self.createGameGrid(self.fr_gamegrid)
        self.lbl_curr_player['text'] = f'Current player: {self.players[self.current_player].name}'

        self.game_loop()

    def game_loop(self):
        """
        Handles the AI in the game.
        """
        if self.players[self.current_player].type == 'ai':
            number = self.players[self.current_player].getInput(self.board)

            ended = self.handle_step(number)

            if ended:
                self.after_cancel(self._loop)
                self._loop = None
                return

        self._loop = self.after(500, self.game_loop)

    def handle_step(self, number):
        """
        Handles the game step of adding the sign to the board and the grid.
        Progresses the game to the next step.

        :param number: the grid number to add the sign to
        """
        self.board.writeField(self.players[self.current_player].sign, number)
        self.label_list[number]['text'] = self.board.signs[
            self.players[self.current_player].sign]

        # Check if the game has ended
        if self.board.isWin(self.players[self.current_player].sign, number):
            messagebox.showinfo('The game has ended',
                f'{self.players[self.current_player].name} has won the game.')
            return True
        # Check if no more fields are free
        elif self.board.isDraw():
            messagebox.showinfo('The game has ended', f'It was a draw')
            return True

        self.current_player = next(self.player_iterator)
        self.lbl_curr_player['text'] = f'Current player: {self.players[self.current_player].name}'

        return False

    # Iterator for going between 0 and 1
    def toggleValue(self):
        while True:
            yield 0
            yield 1


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
