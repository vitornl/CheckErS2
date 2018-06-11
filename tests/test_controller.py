from src.mvc.Controller.rules import Rule
from src.mvc.Model.bot import Bot
from src.mvc.Model.player import Player
from src.mvc.Model.piece import Piece
from src.mvc.Model.board import Board
from unittest.mock import Mock, MagicMock, patch
import pytest

class TestController:
# Testes do Controller
    @patch('src.mvc.Controller.rules.Rule._load_file')
    def test_rules_init(self, load_file_mock):
        args = 'teste'
        rules_with_load = Rule('file', args)
        assert load_file_mock.call_count == 1
        assert load_file_mock.called_with(args)
        rules_wo_load = Rule('human')
        assert load_file_mock.call_count == 1

    def test_rules_load_file(self):
        file_name = "../src/tests/tabuleiro_inicial.txt"
        file = open(file_name, "w")
        contentLine = "0 0 0 0 0 0 0 0\n"
        for i in range(8):
            file.write(contentLine)
        file.close()

        file = open(file_name, "r")
        rules = Rule('human')
        rules._load_file(file)
        for player in rules.players:
            assert len(player.pieces) == 0
        file.close()

        file = open(file_name, "w")
        contentWithPieces = "1 0 2 0 3 0 4 0\n"
        file.write(contentWithPieces)
        for i in range(7):
            file.write(contentLine)
        file.close()

        file = open(file_name, "r")
        rules_with_pieces = Rule('human')
        rules._load_file(file)
        assert len(rules.players[0].pieces) == 2
        assert len(rules.players[1].pieces) == 2
        assert rules.players[0].get_qty_draughts() == 1
        assert rules.players[1].get_qty_draughts() == 1
        file.close()

    def test_rules_set_players(self):
        rules = Rule('human')
        (p1, p2), turn_player = rules._set_players('bot')
        assert type(p1) == Bot or type(p2) == Bot
        (p1, p2), turn_player = rules._set_players('human')
        assert type(p1) == Player and type(p2) == Player

    def test_rules_init_board(self):
        rules = Rule('human')
        rules.board = Board()
        rules._init_board(rules.board, rules.players)
        for i in range(0, 8):
            for j in range(0, 8):
                if i not in (3, 4) and (j + i) % 2 != 0:
                    assert type(rules.board.board[j][i]) == Piece
                else:
                    assert rules.board.board[j][i] is None

    def test_rules_evaluate_position(self):
        rules = Rule('human')
        assert rules._evaluate_position((-1, 0), Piece("p1")) == 0
        assert rules._evaluate_position((8, 0), Piece("p1")) == 0
        assert rules._evaluate_position((0, -1), Piece("p1")) == 0
        assert rules._evaluate_position((0, 8), Piece("p1")) == 0
        assert rules._evaluate_position((0, 0), rules.players[0].pieces[0]) == 1
        assert rules._evaluate_position((1, 0), rules.players[0].pieces[0]) == 0
        assert rules._evaluate_position((0, 5), rules.players[0].pieces[0]) == 2


