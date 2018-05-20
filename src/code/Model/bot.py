import copy
import numpy as np
from .movement import Movement
from .player import Player

class Bot(Player):

    def __init__(self, mode, name='ai', color='blue', side=-1):

        super().__init__(name, color, side)
        self.max_depth = self._set_mode(mode)
        self.next_move = None #jogada a ser feita

    def execute(self, rules, possibilities):
        #preciso acessa uma cópia das regras para fazer as simulações
        #(possíveis movimentos e suas consequências)
        simulator = rules.copy()
        alpha = np.iinfo(np.int32).min
        beta = np.iinfo(np.int32).max
        self._minmax(simulator, alpha, beta, 1, possibilities)

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
    
    def _minmax(self, rules, alpha, beta, depth, possibilities):
        #preciso de acesso ao fim do jogo
        if depth == self.max_depth or rules.who_won(possibilities):
            return self._utilty(rules)

        if rules.turn_player.name == 'ai':
            value = np.iinfo(np.int32).min
            #preciso das possíveis jogadas da ai
            for piece in possibilities:
                for old_movement in possibilities[piece]:
                    simulator = rules.copy()
                    
                    piece_position = old_movement.piece.get_position()
                    piece = simulator.board.get_piece(piece_position)
                    destiny = old_movement.destiny
                    movement = Movement(piece, destiny[0])
                    for dest in destiny[1:]:
                        movement.add_destiny(dest)
                    eliminated = old_movement.eliminated
                    for elim_piece in eliminated:
                        piece_position = elim_piece.get_position()
                        movement.add_elimination(simulator.board.get_piece(piece_position))
                    
                    while True:
                        simulator.move_piece(piece, movement.get_movement())
                        movement.next_movement()
                        if movement.get_movement() == None:
                            if movement.get_eliminateds():
                                # print("ai", movement.get_eliminateds())
                                simulator.eat_pieces(movement)
                            simulator.check_draughts(piece)
                            simulator.next_turn()
                            break

                    new_possibilities = simulator.get_all_possible_moves(simulator.turn_player)
                    tmp = self._minmax(simulator, alpha, beta, depth+1, new_possibilities)
                    
                    if tmp > value:
                        value = tmp
                    if value > alpha:
                        alpha = value
                        candidade_move = old_movement
                    if depth == 1:
                        self.next_move = candidade_move
                    if beta <= alpha:
                        break
            
            return value
        
        else: #turno do inimigo
            value = np.iinfo(np.int32).max
            #preciso das possíveis jogadas do inimigo
            for piece in possibilities:
                '''
                for movement in possibilities[piece]:
                    simulator = rules.copy()
                '''
                for old_movement in possibilities[piece]:
                    simulator = rules.copy()
                    
                    piece_position = old_movement.piece.get_position()
                    piece = simulator.board.get_piece(piece_position)
                    destiny = old_movement.destiny
                    movement = Movement(piece, destiny[0])
                    for dest in destiny[1:]:
                        movement.add_destiny(dest)
                    eliminated = old_movement.eliminated
                    for elim_piece in eliminated:
                        piece_position = elim_piece.get_position()
                        movement.add_elimination(simulator.board.get_piece(piece_position))
                    
                    while True:
                        simulator.move_piece(piece, movement.get_movement())
                        movement.next_movement()
                        if movement.get_movement() == None:
                            if movement.get_eliminateds():
                                # print("player", movement.get_eliminateds())
                                simulator.eat_pieces(movement)
                            simulator.check_draughts(piece)
                            simulator.next_turn()
                            break
                    
                    new_possibilities = simulator.get_all_possible_moves(simulator.turn_player)
                    tmp = self._minmax(simulator, alpha, beta, depth+1, new_possibilities)

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