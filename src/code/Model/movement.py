class Movement:
    def __init__(self, position, location_eliminated_piece):
        self.position = position
        self.location_eliminated_piece = location_eliminated_piece

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_location_eliminated_piece(self):
        return self.location_eliminated_piece

    def set_location_eliminated_piece(self, location_piece):
        self.location_eliminated_piece = piece