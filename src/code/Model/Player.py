from .piece import Piece

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pieces = []

    def set_pieces(self, pieces):
        self.pieces = pieces
