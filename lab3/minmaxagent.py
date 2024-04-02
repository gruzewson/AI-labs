import copy
import math
import random

from connect4 import Connect4
from exceptions import AgentException

def evaluation(connect4, player):
    if connect4.wins == player:
        return 1
    elif connect4.wins is None:
        for four in connect4.iter_fours():
            if four.count(player) == 3:
                return 0.6
            elif four.count(player) == 2:
                return 0.4
            elif four.count(player) == 1:
                return 0.2
        return 0
    else:
        return -1

def minmax(connect4, depth, max_player, initial_player):
    if connect4.game_over or depth == 0:
        return evaluation(connect4, initial_player), random.choice(connect4.possible_drops())

    if max_player:
        max_eval = math.inf
        for m in connect4.possible_drops():
            connect4_copy = copy.deepcopy(connect4)
            connect4_copy.drop_token(m)
            eval, move = minmax(connect4_copy, depth - 1, False, initial_player)
            #print(f"eval max: {eval}")
            max_eval = max(max_eval, eval)
            if max_eval == eval:
                move = m
        return max_eval, move
    else:
        min_eval = -math.inf
        for m in connect4.possible_drops():
            connect4_copy = copy.deepcopy(connect4)
            connect4_copy.drop_token(m)
            eval, move = minmax(connect4_copy, depth - 1, True, initial_player)
            #print(f"eval min: {eval}")
            min_eval = min(min_eval, eval)
            if min_eval == eval:
                move = m
        return min_eval, move

class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        connect4_copy = copy.deepcopy(connect4)
        minimax, move = minmax(connect4_copy, 3, True, self.my_token)
        return move

