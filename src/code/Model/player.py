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

    def get_qty_draughts(self):
        qty = 0
        for piece in self.pieces:
            if piece.is_draughts:
                qty += 1
        return qty
