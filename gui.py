import tkinter as tk
from functools import partial

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.OPTIONS = {
            'Player VS Player': 1, 
            'Player VS AI': 2, 
            'Smart VS Stupid': 3, 
            'Stupid VS Smart': 4, 
            'Smart VS Smart': 5
        }

        self.DIFFICULTY = {
            'Easy': 0,
            'Hard': 1
        }

        self.label_list = []

        self.master = master

        self.var_mode = tk.StringVar(self.master)
        self.var_mode.set('Player VS AI')

        self.var_diff = tk.StringVar(self.master)
        self.var_diff.set('Easy')

        self.master.title('Tic-Tac-Toe')

        self.master.rowconfigure(0, minsize=500, weight=1)
        self.master.columnconfigure(1, minsize=500, weight=1)

        self.fr_controls = tk.Frame(self.master, width=500, relief=tk.RAISED, bd=2)
        self.fr_gamegrid = tk.Frame(self.master)

        # Maybe only make the grid when the game starts
        # self.createGameGrid(self.fr_gamegrid)

        self.btn_start = tk.Button(self.fr_controls, width=18, text='Start Game', command=self.startGame)
        self.om_modes = tk.OptionMenu(self.fr_controls, self.var_mode, *self.OPTIONS.keys())
        self.om_difficulty = tk.OptionMenu(self.fr_controls, self.var_diff, *self.DIFFICULTY.keys())

        self.fr_controls.grid(row=0, column=0, sticky='ns')
        self.fr_gamegrid.grid(row=0, column=1, sticky='nswe')
        self.btn_start.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.om_modes.grid(row=1, column=0, sticky='ew', padx=5)
        self.om_difficulty.grid(row=2, column=0, sticky='ew', padx=5)

    
    def createGameGrid(self, frame):
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

                label = tk.Label(self.fr_grid, text=f"Row {i}\nColumn {j}")
                label.pack(fill=tk.Y, expand=True)
                
                label.bind('<Button-1>', partial(self.handle_click, j+(i*3)))

                self.label_list.append(label)
    
    def handle_click(self, number, event):
        print(f'The button {number} was clicked!')
        self.label_list[number]['text'] = 'O'
    
    def startGame(self):
        mode = self.OPTIONS[self.var_mode.get()]
        diff = self.DIFFICULTY[self.var_diff.get()]

        print(f'Plaiyng mode nr. {mode} with difficulty {diff}')
        self.createGameGrid(self.fr_gamegrid)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
