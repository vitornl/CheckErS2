# coding=utf-8
import sys

from code.Controller.rules import Rule
from code.View.pygame_display import Pygame_Display
from code.View.console_display import Console_Display

def _human_play(rules, display, possibilities):

    print("Digite a peça a ser jogada: ", end='', flush=True)
    piece_position = display.get_position()
    if type(piece_position) != tuple:
        display.quit()
        return
    piece = rules.board.get_piece(piece_position)
    if possibilities and piece in possibilities.keys():

        path = possibilities[piece]

        while len(path) != 0:
            movement = []
            while len(movement) == 0:
                display.print_board(rules.board, piece, path)
            
                print("Digite a posição do movimento da peça: ", end='', flush=True)
                movement_position = display.get_position()
                if type(movement_position) != tuple:
                    display.quit()
                    return

                for mov in path:
                    if mov.get_movement() == movement_position:
                        #Se entrou aqui significa que achou um movimento possível com aquela posição
                        movement.append(mov)

                if len(movement) == 0:
                    if movement_position == piece_position:
                        break
                    print("Posição inválida.")

            if movement_position == piece_position: break
            rules.move_piece(piece, movement_position)

            for mov in movement:
                mov.next_movement()
            
            if (len(movement) == 1) and (movement[0].get_movement() == None):
                path = []
                rules.eat_pieces(movement[0])
                rules.check_draughts(piece)
                rules.next_turn()
                print("Jogada realizada com sucesso.")
            else:
                path = movement
    else:
        print("Selecione uma peça sua que tenha movimentos possíveis.")

def human_vs_human(display):
    rules = Rule('human')
    
    possibilities = rules.get_all_possible_moves(rules.turn_player)
    print("Atenção!!! Digitar posições no formato: coluna linha\n")
    
    end_game = rules.end_game(possibilities)

    while not end_game[0]:

        display.print_board(rules.board, None, None)

        _human_play(rules, display, possibilities)

        possibilities = rules.get_all_possible_moves(rules.turn_player)

    display.quit()
    
    if end_game[1] is None:
        print("A partida terminou empatada!")
    else:
        print("Jogador {} ganhou!".format(end_game[1].name))

def human_vs_bot(display):
    rules = Rule('bot', 'easy')

    possibilities = rules.get_all_possible_moves(rules.turn_player)
    print("Atenção!!! Digitar posições no formato: coluna linha\n")

    end_game = rules.end_game(possibilities)

    while not end_game[0]:

        display.print_board(rules.board, None, None)

        print("--- TURNO: Jogador {} ---".format(rules.turn_player.name))

        if rules.turn_player.name == 'ai':
            movement = rules.turn_player.execute(rules, possibilities)
            piece = movement.get_piece()
            while True:
                rules.move_piece(piece, movement.get_movement())
                movement.next_movement()
                if (movement.get_movement() == None):
                    rules.eat_pieces(movement)
                    rules.check_draughts(piece)
                    rules.next_turn()
                    print("Jogada realizada com sucesso.")
                    break
        else:
            _human_play(rules, display, possibilities)

        possibilities = rules.get_all_possible_moves(rules.turn_player)
        end_game = rules.end_game(possibilities)

    display.quit()
    
    if end_game[1] is None:
        print("A partida terminou empatada!")
    else:
        print("Jogador {} ganhou!".format(end_game[1].name))
    
def main():
    if len(sys.argv) != 3:
        print("Invalid Input")
        return

    display = None

    if sys.argv[1] == "pygame":
        display = Pygame_Display()
    elif sys.argv[1] == "console":
        display = Console_Display()
    else:
        exit(1)

    if sys.argv[2] == "human":
        human_vs_human(display)
    elif sys.argv[2] == "bot":
        human_vs_bot(display)
    else:
        exit(1)

if __name__ == "__main__":
    main()
