from src.mvc.Model.board import Board
from src.mvc.Model.piece import Piece


# content of test_class.py
class TestClass(object):

    def test_board_new_board(self):
        board = Board()
        assert board.board == [[None] * 8 for i in range(8)]

    def test_board_add_piece(self):
        board = Board()
        position = (2, 3)
        piece = Piece("p1")
        board.add_piece(piece, position)
        assert board.get_piece(position).position == position

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