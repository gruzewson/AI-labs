import copy
import math
import random

from connect4 import Connect4
from exceptions import AgentException

def evaluation(connect4, player):
    if connect4.wins == player:
        return 1
    elif connect4.wins is not None:
        return -1
    else:
        score = 0
        center_column = connect4.width // 2

        for col in range(connect4.width):
            tokens_in_col = 0
            while tokens_in_col + 1 < connect4.height and connect4.board[tokens_in_col + 1][center_column] == '_':
                tokens_in_col += 1
            if tokens_in_col > 0:
                score += (1 if col == center_column else 0.5) * tokens_in_col

        for four in connect4.iter_fours():
            player_tokens = four.count(player)
            empty_slots = four.count('_')
            if player_tokens == 3 and empty_slots == 1:
                score += 0.6 / connect4.width
            elif player_tokens == 2 and empty_slots == 2:
                score += 0.4 / connect4.width
            elif player_tokens == 1 and empty_slots == 3:
                score += 0.2 / connect4.width

        max_possible_score = connect4.width * connect4.height
        normalized_score = score / max_possible_score
        return normalized_score



def alphabeta(connect4, depth, alpha, beta, max_player, initial_player):
    if connect4.game_over or depth == 0:
        return evaluation(connect4, initial_player), None

    if max_player:
        max_eval = -math.inf
        best_move = None
        for m in connect4.possible_drops():
            connect4_copy = copy.deepcopy(connect4)
            connect4_copy.drop_token(m)
            eval, _ = alphabeta(connect4_copy, depth - 1, alpha, beta, False, initial_player)
            if eval > max_eval:
                max_eval = eval
                best_move = m
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = math.inf
        best_move = None
        for m in connect4.possible_drops():
            connect4_copy = copy.deepcopy(connect4)
            connect4_copy.drop_token(m)
            eval, _ = alphabeta(connect4_copy, depth - 1, alpha, beta, True, initial_player)
            if eval < min_eval:
                min_eval = eval
                best_move = m
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


class AlphaBetaAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return alphabeta(connect4, 4, -math.inf, math.inf, True, self.my_token)[1]

