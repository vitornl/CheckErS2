from .Game_Rules import Game_Rules
from ..ctx import *

def Message_Handler(message: str) -> str:
    message_code = message
    response_code = codes['error']
    if message_code == codes['start_game']:
        game = Game_Rules()
        response_code = codes['ok']
    elif message_code == codes['select_piece']:
        pass
    elif message_code == codes['exit']:
        break
    return "{code:{},positions:{}}".format(response_code,positions)