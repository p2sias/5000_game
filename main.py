"""
    Author : p2sias
    Date: 07/2021
    Location: Corsica
"""

from packages.game import Game

if __name__ == "__main__":
    game_instance = Game()
    game_instance.showMenu()

    while game_instance.started:
        game_instance.playTurn()