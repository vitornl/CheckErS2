import pygame

from .ctx import *

class Piece(pygame.Surface):
    __slots__ = ('x', 'y', 'parent')
    def __init__(self, parent: pygame.Surface, player: str, x: int, y: int):
        self.x, self.y = x, y
        self.parent = parent
        img = pygame.image.load(base_piece_path.format(player)).convert_alpha()
        pygame.Surface.__init__(self, (tile_size, tile_size))
        self.blit(img, (0, 0))

    def place(self):
        self.parent.blit(self, (self.x*tile_size, self.y*tile_size))

    def move(self, x, y):
        self.x = x
        self.y = y

    def compare(self, x, y):
        return ((self.x == x) & (self.y == y))