import random
import tkinter as tk
from tkinter import messagebox

class GameObject(object):
    """GameObject class. every game component is a GameObject subclass."""

    def __init__(self, canvas:tk.Canvas, body):
        self.body = body
        self.canvas = canvas
    
    def get_position(self):
        """Returns x0, y0, x1, y1"""
        return self.canvas.coords(self.body)

    def move(self, x, y):
        """change the position to the new x, y position"""
        self.canvas.move(self.body, x, y)

    def delete(self):
        """eliminate the object from game canvas"""
        self.canvas.delete(self.body)

    def change_color(self, color:str):
        """Changes the color of the canvas object"""
        self.canvas.itemconfig(self.body, fill=color)


class Ball(GameObject):
    """Ball class"""

    colors = ['yellow', 'blue', 'red', '#a704d9']
    radius = 25
    frame_rate = 40 # milliseconds

    def __init__(self, canvas:tk.Canvas, x, y, color:str='purple'):
        self.speed = 5
        self.direction = [random.choice([1, -1]), -1] # (delta x, delta y)
        super().__init__(canvas, canvas.create_oval(x, y, x + Ball.radius, y+Ball.radius, fill=color))

    def update(self):
        """Updates the ball position"""
        if Game.is_play:
            Game.bat.set_ball()
            self.collide(Game.bricks) # check if there is a collision
            self.canvas.move(self.body, self.speed * self.direction[0], self.speed * self.direction[1])
        self.canvas.after(self.frame_rate, self.update)

    def collide(self, bricks:list["Brick"]) -> "Brick":
        """checks if the ball has collided one of the bricks."""
        x0, y0, x1, y1 = self.get_position()

        # left and right collision detection
        if x0 <= 0:
            self.direction[0] = 1
        elif x1 >= Game.width:
            self.direction[0] = -1

        # top collision detection
        if y0 <= 0:
            self.direction[1] = 1

        # brick collision detection
        for brick in bricks:
            bx0, by0, bx1, by1 = self.canvas.coords(brick.body)
            center = ((x0 + x1)/2, (y0 + y1) / 2)
            if by0 <= center[1] <= by1:
                if center[0] >= bx1:
                    if x0 <= bx1:
                        self.direction[0] = 1
                        brick.hit()
                        self.change_color(brick.color)
                elif center[0] <= bx0:
                    if x1 >= bx0:
                        self.direction[0] = -1
                        brick.hit()
                        self.change_color(brick.color)
            if bx0 <= (x1 + x0) / 2 <= bx1:
                if center[1] <= by0:
                    if y1 >= by0:
                        self.direction[1] = -1
                        brick.hit()
                        self.change_color(brick.color)
                elif center[1] >= by1:
                    if y0 <= by1:
                        self.direction[1] = 1
                        brick.hit()
                        self.change_color(brick.color)


class Bat(GameObject):
    """Bat class"""

    width = 150
    height = 20

    def __init__(self, canvas:tk.Canvas, x, y, color='green'):
        super().__init__(canvas, canvas.create_rectangle(x, y, x + Bat.width, y + Bat.height, fill=color))
        self.speed = 16
        self.ball = Ball(self.canvas, x + (Bat.width - Ball.radius) // 2, y - Ball.radius)

    def set_ball(self):
        """sets the direction of ball considering the collision of the ball with the bat."""
        x0, y0, x1, y1 = self.ball.get_position()
        batx0, baty0, batx1, baty1 = self.canvas.coords(self.body)
        if y1 >= Game.height:
            Game.game_over(is_won=False)
        if batx0 <= (x0 + x1) / 2 <= batx1:
            if y1 >= baty0:
                self.ball.direction[1] = -1
        elif baty0 <= (y0 + y1) / 2 <= baty1:
            if x1 >= batx0:
                self.ball.direction[0] = -1
            elif x0 <= batx1:
                self.ball.direction[0] = 1

    def move(self, event:tk.Event):
        """Moves the ball"""

        if event.keysym == 'space':
            Game.play_pause()
        
        elif Game.is_play: # freezes the bat
            x0, _, x1, _ = self.canvas.coords(self.body)
            if x0 <= 0:
                self.canvas.moveto(self.body, Game.width - Bat.width)
            elif x1 >= Game.width:
                self.canvas.moveto(self.body, 0)

            if event.keysym == "Right":
                self.canvas.move(self.body, self.speed, 0)
            elif event.keysym == "Left":
                self.canvas.move(self.body, -self.speed, 0)


class Brick(GameObject):
    """Brick class"""

    width = 200
    height = 30
    colors = ['yellow', 'blue', 'red', '#a704d9']

    def __init__(self, canvas:tk.Canvas, x:float, y:float, hits:int):
        self.color = self.get_color()
        super().__init__(canvas, canvas.create_rectangle(x, y, x + Brick.width, y + Brick.height, fill=self.color))
        self.hits = hits
        self.label = self.canvas.create_text(x + Brick.width // 2, y + Brick.height // 2, text=str(self.hits), font=("Helvetica", 10, "bold"))
        
    def get_color(self):
        f"""Returns a random color from {Brick.colors}"""
        if len(Brick.colors) == 0:
            Brick.colors = ['yellow', 'blue', 'red']
            random.shuffle(Brick.colors)
        return Brick.colors.pop()

    def hit(self):
        """applies the hit action to the brick."""
        self.hits -= 1
        self.canvas.itemconfig(self.label, text=str(self.hits))
        if not self.hits:
            Game.bricks.remove(self)
            self.canvas.delete(self.label)
            self.delete()
        
        if not len(Game.bricks):
            Game.game_over(is_won=True)


class Game:
    """Game class"""

    is_play = False
    width = 600
    height = 500
    bricks:list[Brick] = []
    bat:Bat = None
    root:tk.Tk = None
    canvas:tk.Canvas = None

    def __init__(self, bg='black'):
        Game.root = tk.Tk()
        Game.root.title("AP4002 Brick Breaker!")
        Game.root.geometry("600x500")
        Game.root.resizable(0, 0)
        Game.canvas = tk.Canvas(Game.root, width=Game.width, height=Game.height, bg=bg)
        Game.canvas.grid(row=0, column=0)
    
    def start_game(self):
        """Starts the game."""
        self.create_objects()
        self.key_handler()
        self.bat.ball.update()
        self.root.mainloop()

    def create_objects(self):
        """Creates the game objects."""
        # creating bricks
        Game.bricks = []
        for layer in range(3, 0, -1):
            for i in range(3):
                Game.bricks.append(Brick(self.canvas, i * 200, (3 - layer) * 30, layer))

        # creating the bat (each bat has one ball)
        Game.bat = Bat(self.canvas, (Game.width - Bat.width) // 2, Game.height - Bat.height)

    def key_handler(self):
        """Binds the keys of the game with specified methods"""
        self.canvas.bind_all('<space>', Game.bat.move)
        self.canvas.bind_all('<Right>', Game.bat.move)
        self.canvas.bind_all('<Left>', Game.bat.move)

    @classmethod
    def game_over(cls, is_won:bool=False):
        """Shows the approperiate message when the game is over."""
        Game.is_play = False
        if is_won:
            messagebox.showinfo("game over", "You won!")
        else:
            messagebox.showinfo("game over", "You lost.")
        cls.canvas.destroy()
        cls.root.destroy()

    @classmethod
    def play_pause(cls):
        """handle the stop action of the game."""
        cls.is_play = False if cls.is_play == True else True


if __name__ == "__main__":
    game = Game('black')
    game.start_game()
