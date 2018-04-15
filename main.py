from display import Display
from board import Board, Player
import pygame

def main():
    
    board = Board()
    display = Display((400, 400), "Checkers")

    p1 = Player('p1', 0, 'red')
    p2 = Player('p2', 1, 'blue')
    players = [p1, p2]

    board.init_board(players)
    display.draw_board(board.board)
    game_exit = False
    clock = pygame.time.Clock()

    player_turn = p1
    while not game_exit:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                game_exit = True
            if (event.type == pygame.MOUSEBUTTONUP):
                board_pos = display.get_board_position(event)
                selected_piece = board.identify_piece(player_turn, board_pos)
                if(selected_piece != None):
                    display.highlight_piece(selected_piece)

        pygame.display.flip()
        clock.tick(30)
        
pygame.quit()

if __name__ == "__main__":
    main()
    