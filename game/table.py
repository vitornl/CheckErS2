import pygame

from .ctx import *
from .piece import *

class Table():
    __slots__ = ("pywin", "img")
    player1, player2 = [], []

    def __init__(self, parent: pygame.Surface):
        self.pywin = parent
        self.img = pygame.image.load(table_path)
        for y in range(3):
            for x in range(4):
                self.player1.append(Piece(self.pywin, player_color[0], 2*x + (y + 1)%2, y))
        for y in range(5, 8):
            for x in range(4):
                self.player2.append(Piece(self.pywin, player_color[1], 2*x + (y + 1)%2, y))
    
    def place(self):
        self.pywin.blit(self.img, (0, 0))

    def update_players(self):
        for piece in self.player1: piece.place()
        for piece in self.player2: piece.place()