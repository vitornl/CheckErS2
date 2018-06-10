from src.mvc.Controller.rules import Rule
from unittest.mock import Mock, MagicMock, patch



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
        file_name = "tests/tabuleiro_inicial.txt"
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
