import numpy as np
from .player import Player

class Bot(Player):

    def __init__(self, mode, name='ai', color='blue', side=-1):

        super(name, color, side)
        self.max_depth = self._set_mode(mode)
        self.next_move = None #jogada a ser feita

    def execute(self, rules):
        #preciso acessa uma cópia das regras para fazer as simulações
        #(possíveis movimentos e suas consequências)
        simulator = rules.make_a_copy()
        alpha = np.iinfo(np.int32).min
        beta = np.iinfo(np.int32).max
        self._minmax(simulator, alpha, beta, 1)

        #proxima jogada, aqui deve ser uma tupla com a peça selecionada e 
        #uma lista de movimentações (caso haja mais de uma é uma eliminação multipla)
        return self.next_move

    def _set_mode(self, mode):

        if mode == 3 or mode == 'hard':
            return 6
        elif mode == 2 or mode == 'normal':
            return 4
        else: #mode == 1 or mode == 'easy'
            return 2
    
    def _minmax(self, rules, alpha, beta, depth):
        #preciso de acesso ao fim do jogo
        if depth == self.max_depth or rules.check_end_game():
            return self._utilty(rules)
        
        if rules.turn_player == self:
            value = np.iinfo(np.int32).min
            #preciso das possíveis jogadas da ai
            possible_moves = rules.possible_moves
            for possible_move in possible_moves:
                #preciso acessa uma cópia das regras para fazer as simulações
                #(possíveis movimentos e suas consequências)
                simulator = rules.make_a_copy()
                simulator.move_piece(possible_move['piece'], possible_move['move'])
                tmp = self._minmax(simulator, alpha, beta, depth+1)
                
                if tmp > value:
                    value = tmp
                if value > alpha:
                    alpha = value
                    candidade_move = possible_move
                if depth == 1:
                    self.next_move = candidade_move
                if beta <= alpha:
                    break
            
            return value
        
        else: #turno do inimigo
            value = np.iinfo(np.int32).max
            #preciso das possíveis jogadas do inimigo
            possible_moves = rules.possible_moves
            for possible_move in possible_moves:
                simulator = rules.make_a_copy()
                simulator.move_piece(possible_move['piece'], possible_move['move'])
                tmp = self._minmax(simulator, alpha, beta, depth+1)

                if tmp < value:
                    value = tmp
                if value < beta:
                    beta = value
                if beta <= alpha:
                    break
            
            return value

    
    def _utilty(self, rules):
        #preciso de acesso às peças do inimigo
        return len(self.pieces) - len(rules.players[1].pieces)