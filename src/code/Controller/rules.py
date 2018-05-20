# coding=utf-8
import copy
from ..Model.board import Board
from ..Model.piece import Piece
from ..Model.player import Player
from ..Model.movement import Movement
from ..Model.bot import Bot

class Rule:

    def __init__(self, mode, *args):
        self.board = Board()
        self.players, self.turn_player = self._set_players(mode, args)
        self._init_board(self.board, self.players)      

    def _set_players(self, mode, *args):
        if mode == 'bot':
            p1 = Bot(args[0][0], 'ai', 'blue', -1)
        else:
            p1 = Player('b', 'blue', -1)
        
        p2 = Player('r', 'red', 1)

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
        """
            Creates a eating path from the last position of the piece after the actual movement

            Parameters
            ----------
            movement: the movement of a piece

            Returns
            -------
            A new movement list or the input movement
        """
        piece = movement.get_piece()
        resp = []
        for i in (-1, 1):
            for j in (-1, 1):
                aux_position = movement.get_last_movement()
                position = [aux_position[0] + i, aux_position[1] + j]
                eval_mov = self._evaluate_position(position, piece)
                if eval_mov == 2:
                    piece_to_jump = self.board.get_piece(position)
                    if movement.check_elimination(piece_to_jump):
                        continue
                    while True:
                        position = (position[0]+i, position[1]+j)
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
                        else:
                            break
                        if not piece.is_draughts:
                            break
        
        return resp

    def _build_movement_draught(self, piece):
        """
            Builder of movement using the piece start position, movement can be walk or jump

            Parameters
            ----------
            piece: Piece that is going to move

            Returns
            -------
            The movement list
        """
        resp = []

        #position evaluator
        for i in (-1, 1):
            for j in (-1, 1):
                for radius in range(1,8):
                    aux_position = piece.get_position()
                    position = [aux_position[0] + i*radius, aux_position[1] + j*radius]
                    eval_mov = self._evaluate_position(position, piece)
                    if eval_mov == 1:
                        mov = Movement(piece, position)
                        resp.append(mov)
                    elif eval_mov == 2:
                        piece_to_jump = self.board.get_piece(position)
                        while True:
                            position = (position[0]+i, position[1]+j)
                            eval_mov = self._evaluate_position(position, piece)
                            if eval_mov == 1:
                                mov = Movement(piece, position)
                                mov.add_elimination(piece_to_jump)
                                aux = self._build_eating_path(mov)
                                if len(aux) > 0:
                                    resp.extend(aux)
                                else:
                                    resp.append(mov)
                            else:
                                break
                        break
                    else:
                        break

        return resp

    def _build_movement_normal(self, piece):
        """
            Builder of movement using the piece start position, movement can be walk or jump

            Parameters
            ----------
            piece: Piece that is going to move

            Returns
            -------
            The movement list
        """
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
                position[1] += piece.player.side
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
        """
            Decide which builder to use

            Parameters
            ----------
            piece: Piece that is going to move

            Returns
            -------
            A Movement list, representing the valid moves of the piece
        """
        if piece.is_draughts:
            return self._build_movement_draught(piece)
        return self._build_movement_normal(piece)

    def _priority_insert(self, eat_list, movement):
        """
            Insert a new eating movement in the list, this creates the higger eating path

            Parameters
            ----------
            eat_list: the movement list
            movement: the new movement to be inserted

            Returns
            -------
            the new eat_list
        """
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
        for key in player.pieces:
            if key in resp and resp[key] == []:
                del resp[key]
        return resp

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
    
    def eat_pieces(self, movement):
        eat_list = movement.get_eliminateds()
        for piece in eat_list:
            self.board.remove_piece(piece)
            piece.player.remove_piece(piece)

    def _other_player(self, player):
        if player is self.players[0]:
            return self.players[1]
        return self.players[0]

    def who_won(self, possibilities):
        """
            Defines who won the game.

            Parameters
            ----------
            possibilities: Movement possibilities of the current turn player
                           => type dict(Piece -> position), where Position is a tuple (int, int)
            Returns
            -------
            Who won the game; None if in this turn there is no winner yet
            => type Player
        """
        if possibilities is None:
            return self._other_player(self.turn_player)
        return None

    def next_turn(self):
        self.turn_player = self._other_player(self.turn_player)

    def copy(self):
        """
            Make a copy of itself.

            Returns
                -------
                A copy of the rule object
        """

        return copy.deepcopy(self)
