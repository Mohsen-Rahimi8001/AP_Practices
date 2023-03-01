class Configuration:
    """This is the configuration of the game. (game mode, difficulty, controllers, player names, hearts)"""
    
    # game modes
    ONEPLAYER_MODE = "oneplayer"
    TWOPLAYER_MODE = "twoplayer"
    GAMEMODES = (ONEPLAYER_MODE, TWOPLAYER_MODE)

    # difficulty levels
    ONEBALL_DIFFICULTY = "oneball"
    MULTIBALL_DIFFICULTY = "multiball"
    DIFFICULTY_LEVELS = (ONEBALL_DIFFICULTY, MULTIBALL_DIFFICULTY)

    # game controllers
    # bind_all code, event.keysym output
    PLAYER1_KEYS = {"Right":("<Right>", "Right"), "Left":("<Left>", "Left")}
    PLAYER2_KEYS = {"Right":("<Key>", "d"), "Left":("<Key>", "a")}
    STOP_KEY = ("<space>", "space")

    def __init__(self, mode:str, difficulty:str, hearts:int, player1Name:str, player2Name:str) -> None:
        """
        initializer of Configuration
        parameters:
            mode: the game mode: (one player, two player)
            difficulty: the game difficulty (one ball multiball)
            hearts: the number of hearts that each player have at the beginning of the game.
            player1Name: the name of player one
            player2Name: the name of player two
        """
        self.mode = mode
        self.difficulty = difficulty
        self.hearts = hearts
        self.player1Name = player1Name
        self.player2Name = player2Name

    def set_mode(self, new_mode:str) -> None:
        """mode setter"""
        if new_mode in self.GAMEMODES:
            self._mode = new_mode
        else:
            raise ValueError(f"{new_mode} is not a valid game mode.")

    def set_difficulty(self, new_difficulty:str) -> None:
        """difficulty setter"""
        if new_difficulty in self.DIFFICULTY_LEVELS:
            self._difficulty = new_difficulty
        else:
            raise ValueError(f"{new_difficulty} is not a valid difficulty level.")

    def set_hearts(self, hearts:int) -> None:
        """hearts setter"""
        if self.difficulty == Configuration.ONEBALL_DIFFICULTY:
            self._hearts = 1
        elif type(hearts) == int and 0 < hearts < 10:
            self._hearts = hearts
        else:
            raise ValueError(message=f"hearts must be an integer between 0 and 10. you entered {hearts}")

    def set_player1(self, name:str):
        """player1 name setter"""
        self._player1Name = name.strip() if name else "Player 1"
    
    def set_player2(self, name:str):
        """player2 name setter"""
        self._player2Name = name.strip() if name else "Player 2"

    mode = property(fget=lambda self : self._mode, fset=set_mode, doc="the game mode: (one player, two player)")
    difficulty = property(fget=lambda self : self._difficulty, fset=set_difficulty, doc="the game difficulty (one ball multiball)")
    hearts = property(fget=lambda self : self._hearts, fset=set_hearts, doc="the number of hearts that each player have at the beginning of the game.")
    player1Name = property(fget=lambda self : self._player1Name, fset=set_player1, doc="player one name")
    player2Name = property(fget=lambda self : self._player2Name, fset=set_player2, doc="player two name")

    def set_default(self):
        """sets the default values for the game configuration"""
        self.dificalty = self.ONEBALL_DIFFICULTY
        self.mode = self.ONEPLAYER_MODE
        self.player1Name = ""
        self.player2Name = ""
        self.hearts = 5

    def __enter__(self):
        return self

    def __exit__(self, exp_type, exp_value, exp_traceback):
        del self
