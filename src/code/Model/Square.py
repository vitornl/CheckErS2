from .Piece import Piece

class Square:
    __slots__ = ('background', 'piece')
    def __init__(self, background: int):
        self.background = background
    
    def push_piece(self, piece: Piece):
        self.piece = piece

    def pop_piece(self) -> Piece:
        piece = self.piece
        self.piece = None
        return piece

    def has_piece(self) -> bool:
        return bool(self.piece)