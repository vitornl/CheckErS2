class Board:
    def __init__(self):
        self.board = self._new_board()

    def _new_board(self):
        board = [[None] * 8 for i in range(8)]
        
        return board
        
    def get_piece(self, position):
        return self.board[position[0]][position[1]]

    def add_piece(self, piece, position):
        piece.set_position(position)
        self.board[piece.position[0]][piece.position[1]] = piece

    def move_piece(self, piece, position):
        self.remove_piece(piece)
        self.add_piece(piece, position)

    def remove_piece(self, piece):
        self.board[piece.position[0]][piece.position[1]] = None
        piece.set_position((None, None))