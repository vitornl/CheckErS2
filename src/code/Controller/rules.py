# coding=utf-8
import copy
from ..Model.board import Board
from ..Model.piece import Piece
from ..Model.player import Player
from ..Model.movement import Movement
from ..Model.bot import Bot

class Rule:

    def __init__(self, mode, args = None):
        """
            Class builder
            
            Parameters
            ----------
            mode : game mode (2 player or bot vs. human)
            args : bot level ('easy', 'normal', 'hard') or a file

            Returns
            -------
            A Rule class object
        """
        self.board = Board()
        if mode == 'file':
            self._load_file(args)
        else:
            self.players, self.turn_player = self._set_players(mode, args)
            self._init_board(self.board, self.players)

    def _load_file(self, fp):
        """
            Class builder
            
            Parameters
            ----------
            file: the board in a file, 0 for empty, 1 and 2 for turn_player, 3 and 4 for other player,
            2 and 4 are draughts

            Returns
            -------
            A Rule class object
        """
        p2 = Player('p2', 'blue', -1)
        p1 = Player('p1', 'red', 1)
        self.players = tuple((p1, p2))
        self.turn_player = p1
        pieces = {}
        pieces[p1] = []
        pieces[p2] = []
        for i in range(8):
            aux = fp.readline()
            line = aux.split(' ')
            for j in range(8):
                elem = int(line[j])
                if elem == 0:
                    continue
                piece = None
                if elem < 3:
                    piece = Piece(p1)
                else:
                    piece = Piece(p2)
                self.board.add_piece(piece, (j, i))
                pieces[piece.player].append(piece)
                if elem%2 == 0:
                    piece.turn_draughts()
        for player in pieces:
            player.set_pieces(pieces[player])

    def _set_players(self, mode, *args):
        """
            Initiator of the players
            
            Parameters
            ----------
            mode : game mode (2 player or bot vs. human)
            *args : bot level ('easy', 'normal', 'hard')

            Returns
            -------
            The created players and the first player that is going to play
        """
        if mode == 'bot':
            p1 = Bot(args, 'ai', 'blue', -1)
        else:
            p1 = Player('p2', 'blue', -1)
        p2 = Player('p1', 'red', 1)

        return (p1, p2), p2

    def _init_board(self, board, players):
        """
            Initiate the pieces in the board and assing them to the players

            Parameters
            ----------
            board: The empty board
            player: The players of the game
        """
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
                position = (aux_position[0] + i, aux_position[1] + j)
                eval_mov = self._evaluate_position(position, piece)
                if eval_mov == 2:
                    piece_to_jump = self.board.get_piece(position)
                    if movement.check_elimination(piece_to_jump):
                        continue
                    while True:
                        position = (position[0]+i, position[1]+j)
                        eval_mov = self._evaluate_position(position, piece)
                        if eval_mov == 1 or (eval_mov == 0 and position == movement.get_piece().get_position()):
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
                    position = (aux_position[0] + i*radius, aux_position[1] + j*radius)
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

    def get_all_possible_moves(self, player):
        """
            Fuction to evaluate the list of valid movement of a player

            Parameters
            ----------
            player: The actual player to evaluate the movement

            Returns
            -------
            A Dictionary({piece:[movement]}), where the keys is a piece able to be moved and
            the valuea are a array of movement, for this piece
        """
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
        """
            Fuction to move a piece to a position in the board

            Parameters
            ----------
            selected_piece: The piece that is going to be moved
            position: The destiny position of the piece
        """
        self.board.move_piece(selected_piece, position)

    def check_draughts(self, piece):
        """
            Execute the draught transformation

            Parameters
            ----------
            piece: The piece to be evaluated
        """
        if piece is not None and piece in self.turn_player.pieces and not piece.is_draughts:
            if self.turn_player.side == -1:
                if piece.get_position()[1] == len(self.board.board) - 1:
                    piece.turn_draughts()
            else:
                if piece.get_position()[1] == 0:
                    piece.turn_draughts()
    
    def eat_pieces(self, movement):
        """
            Operation for eating every jumped piece in the board based in the movement

            Parameters
            ----------
            movement: The finish movement
        """
        eat_list = movement.get_eliminateds()
        for piece in eat_list:
            self.board.remove_piece(piece)
            piece.player.remove_piece(piece)

    def _other_player(self, player):
        """
            Fuction to evaluate a player and return the other player in the game

            Parameters
            ----------
            player: The actual player

            Returns
            -------
            The other player of the game
        """
        if player is self.players[0]:
            return self.players[1]
        return self.players[0]

    def _who_won(self, possibilities):
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

    def _draw_ocurred(self):
        """
            Defines if the game has drawn.

            Returns
            -------
            True if a draw condition happened, false otherwise.
            => type Bool
        """
        # Condition one
        if self.players[0].draw_turns >= 20 and self.players[1].draw_turns >= 20:
            return True

        # Condition two, alterned means one or more draughts vs normal + draught. a stands for alterned, d for draughts
        qty_pieces = [len(self.players[0].pieces), len(self.players[1].pieces)]
        qty_draughts = [self.players[0].get_qty_draughts(), self.players[1].get_qty_draughts()]

        draughts_2_v_2 = qty_pieces[0] == 2 and qty_draughts[0] == 2 and qty_pieces[1] == 2 and qty_draughts[1] == 2

        draughts_2_v_1 = (qty_pieces[0] == 2 and qty_draughts[0] == 2 and qty_pieces[1] == 1 and qty_draughts[1] == 1) or (qty_pieces[0] == 1 and qty_draughts[0] == 1 and qty_pieces[1] == 2 and qty_draughts[1] == 2)

        draughts_1_v_1 = qty_pieces[0] == 1 and qty_draughts[0] == 1 and qty_pieces[1] == 1 and qty_draughts[1] == 1

        alterned_2d_v_2a = (qty_pieces[0] == 2 and qty_draughts[0] == 2 and qty_pieces[1] == 2 and qty_draughts[1] == 1) or (qty_pieces[0] == 2 and qty_draughts[0] == 1 and qty_pieces[1] == 2 and qty_draughts[1] == 2)

        alterned_1d_v_2a = (qty_pieces[0] == 1 and qty_draughts[0] == 1 and qty_pieces[1] == 2 and qty_draughts[1] == 1) or (qty_pieces[0] == 2 and qty_draughts[0] == 1 and qty_pieces[1] == 1 and qty_draughts[1] == 1)

        if draughts_2_v_2 or draughts_2_v_1 or draughts_1_v_1 or alterned_2d_v_2a or alterned_1d_v_2a:
            if self.players[0].draw_turns >= 5 and self.players[1].draw_turns >= 5:
                return True

        return False

    def check_draw_turns(self, piece, movement):
        """
            Checks if the actual movement of a piece contributes to a draw condition. If it does, compute the result.

            Parameters
            ----------
            piece: Piece that has been moved.
                   => type Piece
            movement: Movement that has ocurred in the turn.
                   => type Movement
        """
        eat_list = movement.get_eliminateds()
        if piece.is_draughts and len(eat_list) == 0:
            self.turn_player.draw_turns += 1
        else:
            self.turn_player.draw_turns = 0

    def end_game(self, possibilities):
        """
            Defines the end game conditions

            Parameters
            ----------
            possibilities: Movement possibilities of the current turn player
                           => type dict(Piece -> position), where Position is a tuple (int, int)
            Returns
            -------
            A bool meaning if the game has ended
            and won the game; None if in this turn there is no winner yet
            => type Player
        """
        winner = self._who_won(possibilities)
        if winner is None:
            return self._draw_ocurred(), None
        return True, winner

    def next_turn(self):
        """
            Changes the turn player of the game
        """
        self.turn_player = self._other_player(self.turn_player)

    def copy(self):
        """
            Make a copy of itself.

            Returns
                -------
                A copy of the rule object
        """

        return copy.deepcopy(self)
    
    def export_board(self, fp):

        f = open(fp, 'w')
        out_lines = ['' for i in range(len(self.board.board))]
        for row in self.board.board:
            i = 0 
            for e in row:
                if e == None:
                    w = '0'
                elif e.player.name == 'p2':
                    w = '2' if e.is_draughts else '1'
                else:
                    w = '4' if e.is_draughts else '3'
                out_lines[i] += '{} '.format(w)
                i += 1
        for line in out_lines:
            f.write(line[:len(line)-1] + '\n')
        f.close()
