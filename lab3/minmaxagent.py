import copy
import math
import random

from connect4 import Connect4
from exceptions import AgentException

def evaluation(connect4, player):
    if connect4.wins == player:
        return 1
    elif connect4.wins is None:
        return 0
    else:
        return -1

def minmax(connect4, depth, max_player, initial_player):
    if depth == 0 or connect4.game_over:
        return evaluation(connect4, initial_player), None

    if max_player:
        max_eval = -math.inf
        best_move = None
        for m in connect4.possible_drops():
            connect4_copy = copy.deepcopy(connect4)
            connect4_copy.drop_token(m)
            eval, _ = minmax(connect4_copy, depth - 1, False, initial_player)
            if eval > max_eval:
                max_eval = eval
                best_move = m
        return max_eval, best_move
    else:
        min_eval = math.inf
        worst_move = None
        for m in connect4.possible_drops():
            connect4_copy = copy.deepcopy(connect4)
            connect4_copy.drop_token(m)
            eval, _ = minmax(connect4_copy, depth - 1, True, initial_player)
            if eval < min_eval:
                min_eval = eval
                worst_move = m
        return min_eval, worst_move

class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return minmax(connect4, 4, True, self.my_token)[1]
