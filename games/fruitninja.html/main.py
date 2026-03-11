"""
Main entry point for the Fruit Ninja game
"""
import sys
import pygame
from .game import Game

def main():
    """Main entry point for the game"""
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
