from exceptions import AgentException
import math

def evaluation(connect4, player):
    return 1

def minmax(connect4, depth, max_player, inital_player):
    if connect4.game_over or depth == 0:
        return evaluation(connect4, inital_player)

    if max_player:
        max_eval = math.inf
        for move in connect4.possible_drops():
            #tutaj move jakos trza zrobic
            eval = minmax(connect4, depth - 1, False, inital_player)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = -math.inf
        for move in connect4.possible_drops():
            #tutaj move jakos trza zrobic
            eval = minmax(connect4, depth - 1, True, inital_player)
            min_eval = min(min_eval, eval)
        return min_eval

class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        connect4_copy = connect4
        return minmax(connect4_copy, 3, True, self.my_token)