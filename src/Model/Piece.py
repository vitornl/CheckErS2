from ..ctx import piece_color_1, piece_color_2

def other_piece_color(color: int):
    if color == piece_color_1:
        return piece_color_2
    return piece_color_1

class Piece:
    __slots__ = ('color', 'position', 'evolved')
    def __init__(self, color: int, position: list):
        self.color = color
        self.evolved = False
        self.position = position

    def evolve(self):
        self.evolved = True

    def get_position(self) -> list:
        return self.position

    def set_position(self, position: list):
        self.position = position