from ..Model.board import Board
from ..Model.piece import Piece
from ..Model.player import Player

class Rule:

    def __init__(self):
        self.board = Board()
        self.players, self.turn_player = self._set_players()
        self._init_board(self.board, self.players)

    def _set_players(self):
        p1 = Player('1', 'red')
        p2 = Player('2', 'blue')
        
        return (p1, p2), p1
   
    def _init_board(self, board, players):
        pieces = [Piece(players[0]) for i in range(12)]
        k = 0
        for i in range(5, 8):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j+i%2, i))
                k += 1
        players[0].set_pieces(pieces)

        pieces = [Piece(players[1]) for i in range(12)]
        k = 0
        for i in range(0, 3):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j+i%2, i))
                k += 1
        players[1].set_pieces(pieces)

    def move_piece(self, piece_position, new_position):
        piece = self.board.get_piece(piece_position)

        if piece == None:
            print("Não há peça na casa selecionada!")
            return

        possible_plays = self.get_possible_plays(piece)

        if new_position in possible_plays:
            self.board.move_piece(piece, new_position)
        else:
            print("Jogada inválida!")
    
    def get_possible_plays(self, piece):
        # Aqui as peças só andam para cima, assumindo que o player é o 1
        # Temos que mudar a função para quando tivermos damas, já que elas vão pode andar
        # para os dois lados
        candidate_plays = [(piece.position[0] - 1, piece.position[1] - 1), 
                           (piece.position[0] + 1, piece.position[1] - 1)]

        possible_plays = []

        for i in range(len(candidate_plays)):
            if (self.is_play_possible(candidate_plays[i])):
                possible_plays.append(candidate_plays[i])
        
        return possible_plays
    
    def is_play_possible(self, candidate_play):
        # Condições de contorno do tabuleiro
        if candidate_play[0] < 0 or candidate_play[1] < 0 or candidate_play[0] >= len(self.board.board[0]) or candidate_play[1] >= len(self.board.board):
            return False

        # Condição de ter peça na casa
        piece = self.board.get_piece(candidate_play)

        if piece != None:
            return False
        
        return True

    '''
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
    '''

    def eat_piece(self):
        pass

    def movable_piece(self, piece):
        pass

    def valid_moves(self, piece_position):
        pass

    def valid_pieces(self):
        pass

    def next_turn(self):
        pass