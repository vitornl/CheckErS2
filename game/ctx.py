import pygame

################################## COLORS ######################################
BLACK  = pygame.Color('black')
BLUE   = pygame.Color('blue')
CYAN   = pygame.Color('cyan')
GRAY   = pygame.Color('grey50')
RED    = pygame.Color('red')
MAGENTA = pygame.Color('magenta')
WHITE  = pygame.Color('white')
################################## MACROS ######################################
tile_size = 75
size = 8*tile_size
dim = width, height = size, size
table_path = "game/assets/images/table/{}.png".format(size)
piece_per_player = 4*3
player_color = ['red', 'blue']
base_piece_path = "game/assets/images/piece/{{}}/{}.png".format(tile_size)
################################# METHODS ######################################
def screen_to_pos(x, y):
    return x//tile_size, y//tile_size

def pos_to_index(x, y):
    return y, x