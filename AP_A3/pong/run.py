"""Exrtra featrues of the game are listed in README.md in the main branch"""

import pong

with pong.menu.Menu() as m:
    cnf = m.get_configuration()
    if cnf:
        game = pong.game.GameBoard(cnf)
        game.start_game()
        game.mainloop()
