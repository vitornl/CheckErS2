class Board:
    def __init__(self):
        self.board = self._new_board()

    def _new_board(self):
        board = [[None] * 8 for i in range(8)]
        
        return board

    def init_board(self, players):
        for player in players:
            for piece in player.pieces:
                self._add_piece(piece)

    def _add_piece(self, piece):
        self.board[piece.position[0]][piece.position[1]] = piece

    def identify_piece(self, player, position):
        piece = self._get_board_piece(position)
        if(piece == None or piece.player != player):
            return None
        
        return piece

    def _get_board_piece(self, position):

        return self.board[position[0]][position[1]]

class Piece:
    def __init__(self, player, position):
        self.player = player
        #orientation = walk direction: 0 = north; 1 = south
        self.orientation = self.player.turn
        self.position = position
    
    def is_movable(self, board, new_position):
        if(self.orientation == 0 and #north
            new_position[1] > self.position[1] and #y
            (new_position[0] != self.position[0]-1 or #x
            new_position[0] != self.position[0]+1) and
            new_position != None): #empty
            return False

        elif(self.orientation == 1 and #north
            new_position[1] < self.position[1] and #y
            (new_position[0] != self.position[0]-1 or #x
            new_position[0] != self.position[0]+1) and
            new_position != None): #empty
            return False
        
        return True

class Player:
    def __init__(self, name, turn, color):
        self.name = name
        self.turn = turn
        self.color = color
        self.pieces = self._set_pieces()

    def is_p1(self):
        if(self.turn == 0):
            return True

        return False

    def _set_pieces(self):
        pieces = []
        if(self.is_p1()):
            for i in range(5, 8):
                for j in range(0, 7, 2):
                    pieces.append(Piece(self, (j+i%2, i)))
        else:
            for i in range(0, 3):
                for j in range(0, 7, 2):
                    pieces.append(Piece(self, (j+i%2, i)))
        return pieces