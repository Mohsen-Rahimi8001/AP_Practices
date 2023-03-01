from tkinter import *
from tkinter import messagebox
import random
from .configuration import Configuration
from .menu import Menu


class GameBoard:
    """Game root and canvas are here"""
    # constants
    CANV_COORDS = (500, 400) # h, v
    CNF:Configuration = None

    # class attributes
    isPlay = False
    isGameover = False # it is used to control loops of game
    canvas = None
    root = None
    player1 = None
    player2 = None

    @classmethod
    def game_reset(cls):
        """Set all values the same as they were before the initialization"""
        cls.CNF = None
        cls.isPlay = False
        cls.isGameover = False
        cls.canvas = None
        cls.player1 = None
        cls.player2 = None

    def __init__(self, cnf:Configuration):
        """
        initializer of the GameBoard
            creates game main root and canvas
        parameters: 
            cnf: configuration object for the game
        """
        GameBoard.CNF = cnf
        # create game root
        GameBoard.root = Tk()
        GameBoard.root.title("PONG")
        GameBoard.root.focus_force()
        GameBoard.root.geometry("%dx%d" % self.CANV_COORDS)
        GameBoard.root.resizable(0, 0)
        # create game table
        GameBoard.canvas = Canvas(GameBoard.root, width=self.CANV_COORDS[0], height=self.CANV_COORDS[1], bg="cyan")
        GameBoard.canvas.grid(row=0, column=0)
        # holds the name of players and their hearts
        self.pointFrame = Frame(GameBoard.canvas, bg="cyan")
        GameBoard.canvas.create_window(40, 190, window=self.pointFrame)
        # binds close button of the main root to self.close_game method
        GameBoard.root.protocol("WM_DELETE_WINDOW", self.close_game)

    def close_game(self):
        """it is called when the game is about to close"""
        GameBoard.isPlay = False
        if messagebox.askyesno("Quit", "Do you want to close the game?"):
            GameBoard.isGameover = True
            if GameBoard.CNF.mode == "twoplayer":
                p1 = GameBoard.player1
                p2 = GameBoard.player2
                if int(p1.hearts_lbl.cget("text")) > int(p2.hearts_lbl.cget("text")):
                    messagebox.showinfo("GAME OVER!", f"{p1.name} is the winner.")
                elif int(p1.hearts_lbl.cget("text")) < int(p2.hearts_lbl.cget("text")):
                    messagebox.showinfo("GAME OVER!", f"{p2.name} is the winner.")
                else:
                    messagebox.showinfo("GAME OVER!", "It's a tie. nobody won.")
            GameBoard.root.destroy()
        else:
            GameBoard.isPlay = True

    def start_game(self):
        """Creates game components and starts the game."""
        if GameBoard.CNF.mode == "oneplayer":
            self.player1Hearts = Label(self.pointFrame, text = GameBoard.CNF.hearts, bg="cyan")
            self.player1Hearts.grid(row=0, column=1, sticky="w")
            Label(self.pointFrame, text=f"{GameBoard.CNF.player1Name}: ", bg="cyan").grid(row=0, column=0)
            GameBoard.player1 = Player(1, GameBoard.CNF.player1Name, self.player1Hearts, [(self.CANV_COORDS[0] - Rocket.COORDINATES[0]) // 2, self.CANV_COORDS[1] - Rocket.COORDINATES[1]], 10, "blue")

        elif GameBoard.CNF.mode == "twoplayer":
            Label(self.pointFrame, text=f"{GameBoard.CNF.player1Name}: ", bg="cyan").grid(row=0, column=0)
            Label(self.pointFrame, text=f"{GameBoard.CNF.player2Name}: ", bg="cyan").grid(row=1, column=0)
            self.player1Hearts = Label(self.pointFrame, text = GameBoard.CNF.hearts, bg="cyan")
            self.player1Hearts.grid(row=0, column=1, sticky="w")
            self.player2Hearts = Label(self.pointFrame, text = GameBoard.CNF.hearts, bg="cyan")
            self.player2Hearts.grid(row=1, column=1, sticky="w")
            GameBoard.player1 = Player(1, GameBoard.CNF.player1Name, self.player1Hearts, [0, 390], 10, "blue")
            GameBoard.player2 = Player(2, GameBoard.CNF.player2Name, self.player2Hearts, [0, 0], 10, "red")

        if GameBoard.CNF.difficulty == "multiball":
            GameBoard.canvas.create_oval(self.CANV_COORDS[0] // 2, self.CANV_COORDS[1] // 2, self.CANV_COORDS[0] // 2 \
            + Ball.BALL_DIAMETER, self.CANV_COORDS[1] // 2 + Ball.BALL_DIAMETER)
            self.multiball_handler()
        else:
            ball = Ball([self.CANV_COORDS[0] // 2, self.CANV_COORDS[1] // 2], 2)
            ball.move_ball()
        
        self.key_reader()

    def multiball_handler(self) -> None:
        """Manages creating multiple balls and starts move them"""
        if not GameBoard.isGameover:
            if GameBoard.isPlay:
                ball = Ball([self.CANV_COORDS[0] // 2, self.CANV_COORDS[1] // 2], 2)
                ball.move_ball()
            GameBoard.canvas.after(5000, self.multiball_handler)

    def key_reader(self) -> None:
        """this method bind keys to their specified method"""
        # if the right event and left event have the same key, just one of them should run.
        if self.CNF.PLAYER1_KEYS["Right"][0] != self.CNF.PLAYER1_KEYS["Left"][0]:
            self.canvas.bind_all(self.CNF.PLAYER1_KEYS["Right"][0], self.player1.move_rocket)
        self.canvas.bind_all(self.CNF.PLAYER1_KEYS["Left"][0], self.player1.move_rocket)
        
        if GameBoard.CNF.mode == "twoplayer":
            if self.CNF.PLAYER2_KEYS["Right"][0] != self.CNF.PLAYER2_KEYS["Left"][0]:
                self.canvas.bind_all(self.CNF.PLAYER2_KEYS["Right"][0], self.player2.move_rocket)
            self.canvas.bind_all(self.CNF.PLAYER2_KEYS["Left"][0], self.player2.move_rocket)

        self.canvas.bind_all(self.CNF.STOP_KEY[0], self.play_pause)

    def play_pause(self, event:Event) -> None:
        """play pause action (space)"""
        if event.keysym == self.CNF.STOP_KEY[1]:
            GameBoard.isPlay = False if GameBoard.isPlay else True

    @classmethod
    def gameover(cls, loser:str) -> None:
        """This is called when the game is over"""
        cls.isGameover = True
        cls.root.destroy()
        if messagebox.askyesno("GAME OVER!", f"{loser} lost.\nDo you want to play again?"):
            cls.game_reset()
            with Menu() as m:
                cnf = m.get_configuration()
                if cnf:
                    game = GameBoard(cnf)
                    game.start_game()
                    game.mainloop()

    def mainloop(self) -> None:
        """root main loop"""
        self.root.mainloop()


class Rocket: # player
    """Rocket class"""
    COORDINATES = [120, 12] # h, v

    def __init__(self, first_loc:list, speed:int, color:str) -> None:
        """
        initializer of the Rocket class
        parameters: 
            first_loc: the first location of the rocket
            speed: the speed of the rocket
            color: color of the rocket
        """
        self.body = GameBoard.canvas.create_rectangle(first_loc[0], first_loc[1], first_loc[0] \
            + self.COORDINATES[0], first_loc[1] + self.COORDINATES[1], fill=color)
        self.speed = speed


class Player:
    """Player class, this class is used to move rockets"""
    
    def __init__(self, player_number:int, name:str, hearts_lbl:Label, *rocket_cnf) -> None:
        """
        initializer of the Player class
        parameters: 
            player_number: 1 or 2
            name: player name
            hearts_lbl: tkinter label to show number of remaining hearts.
            rocket_cnf: first_loc:list, speed:int, color:str
        """
        self.name = name
        self.player_number = player_number
        self.hearts_lbl = hearts_lbl
        self.rocket = Rocket(*rocket_cnf)

    def lose(self):
        """it is called when a player looses"""
        hearts = int(self.hearts_lbl.cget("text"))
        if hearts == 1:
            GameBoard.gameover(self.name)
        else:
            self.hearts_lbl['text'] = int(self.hearts_lbl.cget("text")) - 1

    def move_rocket(self, event:Event) -> None:
        """Manages rocket movements"""
        if GameBoard.isPlay:
            if self.player_number == 1:
                if event.keysym == GameBoard.CNF.PLAYER1_KEYS["Right"][1]:
                    GameBoard.canvas.move(self.rocket.body, self.rocket.speed, 0)
                elif event.keysym == GameBoard.CNF.PLAYER1_KEYS["Left"][1]:
                    GameBoard.canvas.move(self.rocket.body, -self.rocket.speed, 0)
            elif self.player_number == 2:
                if event.keysym == GameBoard.CNF.PLAYER2_KEYS["Right"][1]:
                    GameBoard.canvas.move(self.rocket.body, self.rocket.speed, 0)
                elif event.keysym == GameBoard.CNF.PLAYER2_KEYS["Left"][1]:
                    GameBoard.canvas.move(self.rocket.body, -self.rocket.speed, 0)
            elif event.keysym == GameBoard.CNF.STOP_KEY[1]:
                GameBoard.isPlay = False
        elif event.keysym == GameBoard.CNF.STOP_KEY[1]:
            GameBoard.isPlay = True

        # check if the Rocket reached edges. it works well for player one and two.
        x1, _, x2, _ = GameBoard.canvas.coords(self.rocket.body)
        if x2 > GameBoard.CANV_COORDS[0]:
            GameBoard.canvas.moveto(self.rocket.body, -1)
        elif x1 < 0:
            GameBoard.canvas.moveto(self.rocket.body, GameBoard.CANV_COORDS[0]-Rocket.COORDINATES[0]-1)


class Ball:
    """Ball class"""
    BALL_DIAMETER = 20

    def __init__(self, first_loc:list, speed:int) -> None:
        """
        initializer of the Ball class
        parameters: 
            first_loc: the first location of the ball
            speed: the speed of the ball
        """
        self.body = GameBoard.canvas.create_oval(*first_loc, first_loc[0] + self.BALL_DIAMETER, first_loc[1] \
            + self.BALL_DIAMETER, fill="yellow")
        self.speed = speed
        # randomly move at first
        self.xmove = random.choice((-1, 1))
        self.ymove = random.choice((-1, 1))

    def move_ball(self) -> None:
        """Moves the ball"""
        if GameBoard.isGameover:
            del self
            return

        if GameBoard.isPlay:
            x0, y0, x1, y1 = GameBoard.canvas.coords(self.body)
            if x1 > GameBoard.CANV_COORDS[0] or x0 < 0:
                self.xmove *= -1
            if y0 < 0:
                if not GameBoard.player2:
                    self.ymove *= -1
                else:
                    # player 2 lost
                    GameBoard.player2.lose()
                    del self
                    return

            elif y1 > GameBoard.CANV_COORDS[1]:
                # player 1 lost
                GameBoard.player1.lose()
                del self
                return
            
            r1x0, r1y0, r1x1, _ = GameBoard.canvas.coords(GameBoard.player1.rocket.body)
            if x0 >= r1x0 and x1 <= r1x1 and y1 >= r1y0:
                self.ymove *= -1
            
            if GameBoard.player2:
                r2x0, _, r2x1, r2y1 = GameBoard.canvas.coords(GameBoard.player2.rocket.body)
                if x0 >= r2x0 and x1 <= r2x1 and y0 <= r2y1:
                    self.ymove *= -1

            GameBoard.canvas.move(self.body, self.xmove * self.speed, self.ymove * self.speed)
        
        GameBoard.canvas.after(20, self.move_ball)

    def __del__(self):
        GameBoard.canvas.delete(self.body)
        del self
