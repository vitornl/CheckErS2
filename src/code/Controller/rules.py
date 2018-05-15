# coding=utf-8
from ..Model.board import Board
from ..Model.piece import Piece
from ..Model.player import Player
from ..Model.movement import Movement

class Rule:

    def __init__(self):
        self.board = Board()
        self.players, self.turn_player = self._set_players()
        self._init_board(self.board, self.players)      

    def _set_players(self):
        p1 = Player('b', -1)
        p2 = Player('r', 1)

        return (p1, p2), p2

    def _init_board(self, board, players):
        pieces = [Piece(players[0]) for i in range(12)]
        k = 0
        for i in range(0, 3):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j + (i + 1) % 2, i))
                k += 1
        players[0].set_pieces(pieces)

        pieces = [Piece(players[1]) for i in range(12)]
        k = 0
        for i in range(5, 8):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j + (i + 1) % 2, i))
                k += 1
        players[1].set_pieces(pieces)

    def _get_possible_eliminations(self, piece):
        eatable = []
        for p_piece in self.board.get_piece_surroundings(piece):
            if type(p_piece) == Piece and p_piece.player != self.turn_player:
                if p_piece.get_position()[0] < piece.get_position()[0]:
                    if p_piece.get_position()[1] < piece.get_position()[1]:
                        eatable.append(Movement((piece.position[0] - 2, piece.position[1] - 2), \
                        p_piece.get_position()))
                    else:
                        eatable.append(Movement((piece.position[0] - 2, piece.position[1] + 2), \
                        p_piece.get_position()))
                else:
                    if p_piece.get_position()[1] < piece.get_position()[1]:
                        eatable.append(Movement((piece.position[0] + 2, piece.position[1] - 2), \
                        p_piece.get_position()))
                    else:
                        eatable.append(Movement((piece.position[0] + 2, piece.position[1] + 2), \
                        p_piece.get_position()))
        for m_eating in eatable:
            if not self.is_movement_possible(m_eating):
                eatable.remove(m_eating)
            else: print(m_eating.get_position())

        return eatable

    def _evaluate_position(self, position, piece):
        """
            Evaluate a position

            Parameters
            ----------
            position: The position to be evaluated
            piece: The piece that is going to this position

            Returns
            -------
            0 - invalid position
            1 - empty position
            2 - enemy piece in the position
        """
        if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
            return 0

        aux_piece = self.board.get_piece(position)

        if aux_piece != None:
            if not aux_piece.player is piece.player:
                return 2
            return 0
        return 1

    def _build_eating_path(self, movement):
        piece = movement.get_piece()
        resp = []
        for i in (-1, 1):
            for j in (-1, 1):
                aux_position = movement.get_movement()
                position = [aux_position[0] + i, aux_position[1] + j]
                eval_mov = self._evaluate_position(position, piece)
                if eval_mov == 2:
                    piece_to_jump = self.board.get_piece(position)
                    if movement.check_elimination(piece_to_jump):
                        continue
                    position[0] += i
                    position[1] += j
                    eval_mov = self._evaluate_position(position, piece)
                    if eval_mov == 1:
                        mov = movement.copy_movement()
                        mov.add_destiny(position)
                        mov.add_elimination(piece_to_jump)
                        aux = self._build_eating_path(mov)
                        if len(aux) > 0:
                            resp.extend(aux)
                        else:
                            resp.append(mov)
        
        return resp

    def _build_movement_draught(self, piece):
        return []

    def _build_movement_normal(self, piece):
        resp = []

        #front movement evaluation
        for i in (-1, 1):
            aux_position = piece.get_position()
            position = [aux_position[0] + i, aux_position[1] - piece.player.side]
            eval_mov = self._evaluate_position(position, piece)
            if eval_mov == 1:
                mov = Movement(piece, position)
                resp.append(mov)
            elif eval_mov == 2:
                piece_to_jump = self.board.get_piece(position)
                position[0] += i
                position[1] -= piece.player.side
                eval_mov = self._evaluate_position(position, piece)
                if eval_mov == 1:
                    mov = Movement(piece, position)
                    mov.add_elimination(piece_to_jump)
                    aux = self._build_eating_path(mov)
                    if len(aux) > 0:
                        resp.extend(aux)
                    else:
                        resp.append(mov)
        
        #backward eating evaluation
        for i in (-1, 1):
            aux_position = piece.get_position()
            position = [aux_position[0] + i, aux_position[1] + piece.player.side]
            eval_mov = self._evaluate_position(position, piece)
            if eval_mov == 2:
                piece_to_jump = self.board.get_piece(position)
                position[0] += i
                position[1] -= piece.player.side
                eval_mov = self._evaluate_position(position, piece)
                if eval_mov == 1:
                    mov = Movement(piece, position)
                    mov.add_elimination(piece_to_jump)
                    aux = self._build_eating_path(mov)
                    if len(aux) > 0:
                        resp.extend(aux)
                    else:
                        resp.append(mov)

        return resp
                

    
    def _build_movement(self, piece):
        if piece.is_draughts:
            return self._build_movement_draught(piece)
        return self._build_movement_normal(piece)

    def _priority_insert(self, eat_list, movement):
        if len(eat_list) == 0:
            eat_list.append(movement)
        else:
            eat = eat_list[0]
            if len(eat.get_eliminateds()) <= len(movement.get_eliminateds()):
                if len(eat.get_eliminateds()) < len(movement.get_eliminateds()):
                    eat_list = []
                eat_list.append(movement)
        return eat_list
            
    # Pega possibilidades de jogadas, mapeadas como um dicionário Peça -> Lista de Jogadas
    # A lista de jogada é uma lista de tuplas com posições possíveis   
    def get_all_possible_moves(self, player):
        resp = {}
        walk = []
        eat = []
        for piece in player.pieces:
            piece_movement = self._build_movement(piece)
            if len(piece_movement) > 0: resp[piece] = []
            for mov in piece_movement:
                if len(mov.get_eliminateds()) > 0:
                    eat = self._priority_insert(eat, mov)
                else:
                    walk.append(mov)
        
        if len(eat) > 0:
            for mov in eat:
                resp[mov.get_piece()].append(mov)
        elif len(walk) > 0:
            for mov in walk:
                resp[mov.get_piece()].append(mov)
        if len(resp) == 0:
            return None
        return resp

    # Pega lista de movimentos possíveis para uma peça em particular, dependendo se é peça normal ou dama
    # def _get_piece_moves(self, piece):
    #     if not piece.is_draughts:
    #         possible_movements = self._get_normal_moves(piece)
    #     #else:
    #         #possible_movements = self._get_draught_moves(piece)

    #     return possible_movements

    # Pega movimentos de uma peça normal
    # def _get_normal_moves(self, piece):
    #     possible_movements = []
        
    #     if self.turn_player == self.players[1]:  # Player r jogando
    #         candidate_mov_1 = Movement((piece.position[0] - 1, piece.position[1] - 1), None)
    #         candidate_mov_2 = Movement((piece.position[0] + 1, piece.position[1] - 1), None)

    #         #Caso o movimento não seja possível por conta de uma peça adversária,
    #         #é necessário ver possibilidade de pular sobre peça
            
    #         if not self.is_movement_possible(candidate_mov_1): 
    #             possiblePiece = self.board.get_piece(candidate_mov_1.get_position())
    #             if possiblePiece != None:
    #                 if possiblePiece.player != self.players[1]:
    #                     candidate_mov_1 = Movement((piece.position[0] - 2, piece.position[1] - 2)
    #                                 ,candidate_mov_1.get_position())         

    #         if not self.is_movement_possible(candidate_mov_2):
    #             possiblePiece = self.board.get_piece(candidate_mov_2.get_position())
    #             if possiblePiece != None:
    #                 if possiblePiece.player != self.players[1]:
    #                     candidate_mov_2 = Movement((piece.position[0] + 2, piece.position[1] - 2)
    #                                         ,candidate_mov_2.get_position())
            
    #     else:  # Player b jogando
            
    #         candidate_mov_1 = Movement((piece.position[0] - 1, piece.position[1] + 1), None)
    #         candidate_mov_2 = Movement((piece.position[0] + 1, piece.position[1] + 1), None)

    #         if not self.is_movement_possible(candidate_mov_1):
    #             possiblePiece = self.board.get_piece(candidate_mov_1.get_position())
    #             if possiblePiece != None:
    #                 if possiblePiece.player != self.players[0]:
    #                     candidate_mov_1 = Movement((piece.position[0] - 2, piece.position[1] + 2),
    #                                                 candidate_mov_1.get_position())

    #         if not self.is_movement_possible(candidate_mov_2): 
    #             possiblePiece = self.board.get_piece(candidate_mov_2.get_position())
    #             if possiblePiece != None:
    #                 if possiblePiece.player != self.players[0]:
    #                     candidate_mov_2 = Movement((piece.position[0] + 2, piece.position[1] + 2),
    #                                                 candidate_mov_2.get_position())

    #     for movement in [candidate_mov_1, candidate_mov_2]:
    #         if self.is_movement_possible(movement):
    #             possible_movements.append(movement)
        
    #     return possible_movements

    # Pega movimento de uma dama
    def _get_draught_moves(self, piece):
        possible_movements = []
        for i in range(4):
            candidate_movement = self.get_draught_candidate_movement(piece.get_position(), i)

            while self.is_movement_possible(candidate_movement):
                possible_movements.append(candidate_movement)
                candidate_movement = self.get_draught_candidate_movement(candidate_movement, i)

        return possible_movements

    # Pega movimento candidato de dama. Candidato atual é o ponto de partida para o próximo candidato
    # O índice de iteração decide qual orientação está sendo buscada
    def get_draught_candidate_movement(self, actual_candidate, index):
        if index == 0:  # Noroeste
            candidate_movement = (actual_candidate[0] - 1, actual_candidate[1] - 1)
        elif index == 1:  # Nordeste
            candidate_movement = (actual_candidate[0] + 1, actual_candidate[1] - 1)
        elif index == 2:  # Sudoeste
            candidate_movement = (actual_candidate[0] - 1, actual_candidate[1] + 1)
        elif index == 3:  # Sudeste
            candidate_movement = (actual_candidate[0] + 1, actual_candidate[1] + 1)

        return candidate_movement

    # Checa se o movimento é possível, de acordo com as condições de contorno e ocupação de uma casa
    def is_movement_possible(self, possible_move):

        candidate_play = possible_move.get_position()

        # Condições de contorno do tabuleiro
        if candidate_play[0] < 0 or candidate_play[1] < 0 or candidate_play[0] >= len(self.board.board[0]) or \
                candidate_play[1] >= len(self.board.board):
            return False
        # Condição de ter peça na casa
        piece = self.board.get_piece(candidate_play)
        if piece is not None:
            return False

        return True

    def move_piece(self, selected_piece, position):
        self.board.move_piece(selected_piece, position)

    # Checa e executa virada de dama
    def check_draughts(self, piece):
        if piece is not None and piece in self.turn_player.pieces and not piece.is_draughts:
            if self.turn_player.name == 'b':
                if piece.get_position()[1] == len(self.board.board) - 1:
                    piece.turn_draughts()
            else:
                if piece.get_position()[1] == 0:
                    piece.turn_draughts()

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
    
    def eat_piece(self, movement):
        piece = self.board.get_piece(movement.get_location_eliminated_piece())
        old_position = piece.get_position()
        self.board.remove_piece(piece)
        if self.turn_player == self.players[0]:
            player = self.players[1]
        else:
            player = self.players[0]
        player.remove_piece(old_position)
    
    '''
    def movable_piece(self, piece):
        neighborhood = self.board.get_surroundings(piece)
        for neighbor in neighborhood:
            if neighbor is None:
                return True
            if not neighbor.player is piece.player:
                return True
        return False
    '''

    def valid_moves(self, piece_position):
        pass

    def valid_pieces(self):
        pass

    def _other_player(self, player):
        if player is self.players[0]:
            return self.players[1]
        return self.players[0]

    def win_condition(self):
        for player in self.players:
            possibilities = self.get_all_possible_moves(self.turn_player)
            if len(player.pieces) > 0:
                aux = 0
                for piece in player.pieces:
                    aux += 1
                    if possibilities.__contains__(piece):
                        break
                if aux == len(player.pieces):
                    return self._other_player(player)
            else:
                return self._other_player(player)
        return None

    def next_turn(self):
        self.turn_player = self._other_player(self.turn_player)
