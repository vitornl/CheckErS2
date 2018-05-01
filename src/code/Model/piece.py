class Piece:
    def __init__(self, player):
        self.player = player
        self.is_draughts = False
        self.position = (None, None)
    
    def turn_draughts(self):
        self.is_draughts = True

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
