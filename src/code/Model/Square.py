from .Piece import Piece

class Square:
    __slots__ = ('background', 'piece')
    def __init__(self, background):
        self.background = background
    
    def push_piece(self, piece):
        self.piece = piece

    def pop_piece(self):
        piece = self.piece
        self.piece = None
        return piece

    def has_piece(self):
        return bool(self.piece)