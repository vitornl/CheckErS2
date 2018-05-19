from .piece import Piece

class Player:
    def __init__(self, name, color, side):
        self.name = name
        self.color = color
        self.side = side
        self.pieces = []
        self.draw_turns = 0

    def set_pieces(self, pieces):
        self.pieces = pieces
    
    def remove_piece(self, piece):
        self.pieces.remove(piece)
