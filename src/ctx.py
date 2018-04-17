import itertools
############################## GAME DATA    ##############################
piece_color_1 = 0
piece_color_2 = 1
num_pieces = 12
############################## TABLE    ##############################
squares = 8
background_colors = itertools.cycle([0, 1])
############################## Server    ##############################
codes = {
    'exit':666,
    'ok':200,
    'start_game':100,
    'select_piece':101,
    'invalid_piece':102,
    'highlight':103,
    'destiny_position':104,
    'next_turn':105,
    'error':-1
}