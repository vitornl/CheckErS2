from src.mvc.Model.board import Board
from src.mvc.Model.piece import Piece
from src.mvc.Model.player import Player
from src.mvc.Model.movement import Movement
from src.mvc.Model.bot import Bot
from src.mvc.Controller.rules import Rule
from unittest.mock import Mock, MagicMock, patch
import numpy as np

class TestModel(object):

    # Testes do Modelo
    def test_piece_turn_draughts(self):
        piece = Piece("p1")
        piece.turn_draughts()
        assert piece.is_draughts

    def test_piece_get_position(self):
        piece = Piece("p1")
        assert piece.get_position() == piece.position

    def test_piece_set_position(self):
        piece = Piece("p1")
        position = (0, 0)
        piece.set_position(position)
        assert piece.get_position() == piece.position

    def test_player_set_pieces(self):
        player = Player("p1", "red", 1)
        pieces = [Piece("p1"), Piece("p1")]
        player.set_pieces(pieces)
        assert player.pieces == pieces

    def test_player_remove_pieces(self):
        player = Player("p1", "red", 1)
        removed_piece = Piece("p1")
        pieces = [removed_piece, Piece("p1"), Piece("p1")]
        player.set_pieces(pieces)
        player.remove_piece(pieces[0])
        assert len(player.pieces) == 2
        assert removed_piece not in player.pieces

    def test_player_get_qty_draughts(self):
        player = Player("p1", "red", 1)
        assert player.get_qty_draughts() == 0
        pieces = [Piece("p1") for i in range(5)]
        player.set_pieces(pieces)
        assert player.get_qty_draughts() == 0
        player.pieces[0].turn_draughts()
        assert player.get_qty_draughts() == 1

    def test_board_new_board(self):
        board = Board()
        assert board.board == [[None] * 8 for i in range(8)]

    def test_board_add_piece(self):
        board = Board()
        position = (0, 0)
        piece = Piece("p1")
        board.add_piece(piece, position)
        assert board.get_piece(position).get_position() == position

    def test_board_get_piece(self):
        board = Board()
        board.add_piece(Piece("p1"), (0, 0))
        assert board.get_piece((-1, 0)) is None
        assert board.get_piece((8, 0)) is None
        assert board.get_piece((0, -1)) is None
        assert board.get_piece((0, 8)) is None
        assert board.get_piece((0, 0)) is not None

    def test_board_move_piece(self):
        board = Board()
        piece = Piece("p1")
        board.add_piece(piece, (0,0))
        new_position = (0, 5)
        board.move_piece(piece, new_position)
        assert board.get_piece(new_position).position == new_position

    def test_board_remove_piece(self):
        board = Board()
        position = (0, 0)
        board.add_piece(Piece("p1"), position)
        piece = board.get_piece(position)
        board.remove_piece(piece)
        assert board.get_piece(position) is None

    def test_movement_get_piece(self):
        piece = Piece("p1")
        mov = Movement(piece, (0, 0))
        assert mov.get_piece() == piece

    def test_movement_destiny(self):
        added_destiny = (3, 3)
        mov = Movement(Piece("p1"), (1, 1))
        mov.add_destiny(added_destiny)
        assert mov.destiny[-1] == added_destiny

    def test_movement_add_elimination(self):
        added_elimination = Piece("p2")
        mov = Movement(Piece("p1"), (1, 1))
        mov.add_elimination(added_elimination)
        assert mov.eliminated[-1] == added_elimination

    def test_movement_next_movement(self):
        mov = Movement(Piece("p1"), (0, 0))
        new_destiny = (2, 2)
        mov.add_destiny(new_destiny)
        mov.next_movement()
        assert mov.destiny[0] == new_destiny

    def test_movement_get_eliminateds(self):
        mov = Movement(Piece("p1"), (0, 0))
        eliminateds = [Piece("p2")]
        mov.add_elimination(eliminateds[0])
        assert mov.get_eliminateds() == eliminateds

    def test_movement_get_movement(self):
        destiny = (2, 0)
        mov = Movement(Piece("p1"), destiny)
        assert mov.get_movement() == destiny
        mov.next_movement()
        assert mov.get_movement() is None

    def test_movement_get_last_movement(self):
        first_destiny = (2, 0)
        last_destiny = (0, 2)
        mov = Movement(Piece("p1"), first_destiny)
        mov.add_destiny(last_destiny)
        assert mov.get_last_movement() == last_destiny
        mov.next_movement()
        mov.next_movement()
        assert mov.get_last_movement() is None

    def test_movement_check_destiny(self):
        first_destiny = (0, 0)
        false_destiny = (2, 0)
        mov = Movement(Piece("p1"), first_destiny)
        assert mov.check_destiny(first_destiny)
        assert not mov.check_destiny(false_destiny)

    def test_movement_check_elimination(self):
        true_elimination = Piece("p2")
        false_elimination = Piece("p2")
        mov = Movement(Piece("p1"), (2, 2))
        mov.add_elimination(true_elimination)
        assert mov.check_elimination(true_elimination)
        assert not mov.check_elimination(false_elimination)

    def test_movement_copy_movement(self):
        mov = Movement(Piece("p1"), ())
        mov_copy = mov.copy_movement()
        assert mov.piece == mov_copy.piece and mov.destiny == mov_copy.destiny and mov.eliminated == mov_copy.eliminated
        mov.add_destiny((2, 5))
        mov_copy = mov.copy_movement()
        assert mov.piece == mov_copy.piece and mov.destiny == mov_copy.destiny and mov.eliminated == mov_copy.eliminated
        mov.add_elimination(Piece("p2"))
        mov_copy = mov.copy_movement()
        assert mov.piece == mov_copy.piece and mov.destiny == mov_copy.destiny and mov.eliminated == mov_copy.eliminated

    def test_bot_set_mode(self):
        bot_easy = Bot("easy")
        assert bot_easy.max_depth == 2
        bot_normal = Bot("normal")
        assert bot_normal.max_depth == 4
        bot_hard = Bot("hard")
        assert bot_hard.max_depth == 6

    def test_bot_utility(self):
        bot = Bot("")
 
        contentLine = "0 0 0 0 0 0 0 0\n"
        file = open("tabuleiro_inicial", "w")
        contentWithPieces = "1 0 2 0 3 0 4 0\n"
        file.write(contentWithPieces)

        for i in range(7):
            file.write(contentLine)
 
        file.close()
        rules = Rule(file)
        bot.set_pieces(rules.players[0].pieces)
        assert bot._utility(rules) == 0

    def test_bot_execute(self):
        bot = Bot('normal')
        
        file = open("tabuleiro_inicial", "w")
        file.write("0 0 0 0 0 0 0 0\n")
        file.write("0 0 0 0 0 0 0 0\n")
        file.write("0 0 0 0 0 0 0 0\n")
        file.write("0 0 0 0 0 0 0 0\n")
        file.write("0 0 0 1 0 0 0 0\n")
        file.write("0 0 3 0 3 0 0 0\n")
        file.write("0 0 0 0 0 0 0 0\n")
        file.write("3 0 0 0 0 0 0 0\n")
        file.close()

        file = open("tabuleiro_inicial", "r")
        rules = Rule('file', file)
        file.close()

        bot.set_pieces(rules.players[0].pieces)
        possibilities = rules.get_all_possible_moves(rules.players[0])

        rules.turn_player = rules.players[0]
        
        assert bot.execute(rules, possibilities).get_movement() == (1,6)