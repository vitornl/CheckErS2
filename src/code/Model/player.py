from .piece import Piece

class Player:
    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.pieces = []

    def set_pieces(self, pieces):
        self.pieces = pieces
    
    def remove_piece(self, piece):
        self.pieces.remove(piece)
