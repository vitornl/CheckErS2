# coding=utf-8
import sys

from mvc.Controller.rules import Rule
from mvc.View.pygame_display import Pygame_Display
from mvc.View.console_display import Console_Display

def _human_play(rules, display, possibilities):
    """
        Loop for the game movement of a human player
        
        Parameters
        ----------
        display: Where the game is running
        possibilites: the list of valid plays of that player
    """
    print("Digite a peça a ser jogada: ", end='', flush=True)
    piece_position = display.get_position()
    if type(piece_position) != tuple:
        display.quit()
        return
    piece = rules.board.get_piece(piece_position)
    if possibilities and piece in possibilities.keys():

        moved = False

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
                    if movement_position == piece_position and not moved:
                        break
                    print("Posição inválida.")

            if movement_position == piece_position and not moved:
                break

            rules.move_piece(piece, movement_position)
            moved = True

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

def _game_loop(rules, display):
    """
        The game loop
        
        Parameters
        ----------
        display: Where the game is running
    """
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
    if len(sys.argv) < 2 :
        print("Invalid Input")
        return

    display = None
    rules = None
    
    if sys.argv[1] == "pygame":
        display = Pygame_Display()
        while(rules == None):
            main_menu_option_choosen = display.main_menu()
            if main_menu_option_choosen == "start":
                start_menu_option_choosen = display.start_menu()
                if start_menu_option_choosen == "twoPlayers": rules = Rule('human')
                elif start_menu_option_choosen == "vsComputer": rules = Rule('bot','hard')
                
            elif main_menu_option_choosen == "exit":
                display.quit()
                return

    elif sys.argv[1] == "console":
        display = Console_Display()
        if sys.argv[2] == "human":
            rules = Rule('human')
        elif sys.argv[2] == "bot":
            rules = Rule('bot', 'easy')
        else:
            exit(1)
    else:
        exit(1)

    _game_loop(rules, display)

if __name__ == "__main__":
    main()
