from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from .configuration import Configuration

class Menu:
    """The first menu of the game which collects game configuration and applies them."""
    BACKGROUND_COLOR = "cyan"
    cnf = None

    def show_menu(self):
        """create menu root and place menu components in it"""
        # root configuration
        self.root = Tk()
        self.root.focus_force()
        self.root.title("PONG")
        self.root.geometry("330x280")
        self.root.resizable(0, 0)
        self.root.configure(background=self.BACKGROUND_COLOR)

        # Page header
        Label(self.root, text="Game Configuration", font=("Helvetica", 22, "bold"), fg='#d1c63c', \
            bg=self.BACKGROUND_COLOR).grid(row=0, column=0, columnspan=2, pady=10)

        # get player names
        self.lblPlayer1Name = Label(self.root, text="Player 1: ", font=("Helvetica", 10, "bold"), bg="cyan")
        self.lblPlayer2Name = Label(self.root, text="Player 2: ", font=("Helvetica", 10, "bold"), bg="cyan")
        self.entPlayer1Name = Entry(self.root, width=23)
        self.entPlayer1Name.insert(0, "Player 1")
        self.entPlayer2Name = Entry(self.root, width=23)
        self.entPlayer2Name.insert(0, "Player 2")

        # game mode Combobox and label
        self.lblGameMode = Label(self.root, text="Mode: ", font=("Helvetica", 10, "bold"), bg="cyan")
        self.gameMode = StringVar()
        self.comboGameMode = ttk.Combobox(self.root, textvariable=self.gameMode, state='readonly')
        self.comboGameMode['values'] = Configuration.GAMEMODES
        self.comboGameMode.current(0)

        # game difficulty Combobox and label
        self.lblDifficulty = Label(self.root, text="Difficulty: ", font=("Helvetica", 10, "bold"), bg="cyan")
        self.difficulty = StringVar()
        self.comboDifficulty = ttk.Combobox(self.root, textvariable=self.difficulty, state='readonly')
        self.comboDifficulty['values'] = Configuration.DIFFICULTY_LEVELS
        self.comboDifficulty.current(0)

        # hearts Combobox and label
        self.lblHearts = Label(self.root, text="Hearts: ", font=("Helvetica", 10, "bold"), bg="cyan")
        self.hearts = IntVar()
        self.comboHearts = ttk.Combobox(self.root, textvariable=self.hearts, state='readonly')
        self.comboHearts["values"] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.comboHearts.current(4) # 5 hearts default
        
        # start button
        self.btnStart = ttk.Button(self.root, text="Start", width=22, command=self.btn_start_game)

        # reset button
        self.btnReset = ttk.Button(self.root, text="Reset", width=22, command=self.btn_reset_page)

        self.grid_system()
        self.root.mainloop()
    
    def grid_system(self):
        """Places all visual components in the root grid system"""
        self.lblGameMode.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.comboGameMode.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.lblDifficulty.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.comboDifficulty.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        self.lblHearts.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.comboHearts.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.lblPlayer1Name.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entPlayer1Name.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        self.lblPlayer2Name.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.entPlayer2Name.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.btnReset.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.btnStart.grid(row=6, column=1, padx=10, pady=10, sticky="w")
    
    def configure_game(self) -> bool:
        """
        description: configures the game with new information.
        retrun: if the configuration are initialized correctly returns True else False
        """
        if self.difficulty.get() == Configuration.ONEBALL_DIFFICULTY:
            if self.hearts.get() > 1:
                if messagebox.askokcancel("Wrong configuration!", "You have one ball, you cannot set hearts greater than the number of balls!\n"
                    "set the 1 for hearts?"):
                    self.hearts.set(1)
                else:
                    return False
        self.cnf = Configuration(self.gameMode.get(), self.difficulty.get(), \
            self.hearts.get(), self.entPlayer1Name.get(), self.entPlayer2Name.get())
        return True

    def btn_start_game(self):
        """returns the configuration object the game"""
        if self.configure_game():
            self.root.destroy()

    def get_configuration(self):
        """calls whatever needed to configure the game and returns the configuration object"""
        self.show_menu()
        return self.cnf
    
    def btn_reset_page(self):
        """reset the page to default"""
        self.comboDifficulty.current(0)
        self.comboGameMode.current(0)
        self.comboHearts.current(4)
        self.entPlayer1Name.delete(0, END)
        self.entPlayer1Name.insert(0, "Player 1")
        self.entPlayer2Name.delete(0, END)
        self.entPlayer2Name.insert(0, "Player 2")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self
