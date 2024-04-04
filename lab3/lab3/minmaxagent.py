import copy
import math
import random

from connect4 import Connect4
from exceptions import AgentException

def evaluation(connect4, player, move):

    if connect4.wins == player:
        return 1
    elif connect4.wins is None:
        center_y = connect4.height // 2
        center_x = connect4.width // 2
        if(connect4.width % 2 == 0):
            center_x += 0.5
        if (connect4.height % 2 == 0):
            center_y += 0.5

        n_row = 0
        while n_row + 1 < connect4.height and connect4.board[n_row + 1][move] == '_':
            n_row += 1
        dist_to_center = math.sqrt((center_x - move)**2 + (center_y - n_row)**2)
        #print(f" move: {move} , {1 / dist_to_center}")
        # for four in connect4.iter_fours():
        #     if four.count(player) == 3:
        #         return 0.6
        #     elif four.count(player) == 2:
        #         return 0.4
        #     elif four.count(player) == 1:
        #         return 0.2
        if dist_to_center != 0:
            return 1 / dist_to_center
        else:
            return 1
    else:
        return -1

def minmax(connect4, depth, max_player, initial_player):
    if connect4.game_over or depth == 0:
        center_column = connect4.width // 2
        if center_column in connect4.possible_drops():
            move = center_column
        else:
            move = connect4.possible_drops()[0]
        return evaluation(connect4, initial_player, move), move

    if max_player:
        max_eval = -math.inf
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
        min_eval = math.inf
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
        minimax, move = minmax(connect4_copy, 4, True, self.my_token) #4 is optimal
        return move

