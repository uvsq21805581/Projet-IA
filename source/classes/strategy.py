import copy
import math
import random
from math import log, sqrt, inf
from random import randrange
import numpy as np
from rich.table import Table
from rich.progress import track
from rich.console import Console
from rich.progress import Progress

import classes.logic as logic

# When implementing a new strategy add it to the `str2strat`
# dictionary at the end of the file


class PlayerStrat:
    def __init__(self, _board_state, player):
        self.root_state = _board_state
        self.player = player

    def start(self):
        """
        This function select a tile from the board.

        @returns    (x, y) A tuple of integer corresponding to a valid
                    and free tile on the board.
        """
        raise NotImplementedError

class Node(object):
    """
    This class implements the main object that you will manipulate : nodes.
    Nodes include the state of the game (i.e. the 2D board), children (i.e. other children nodes), a list of
    untried moves, etc...
    """
    def __init__(self, board, move=(None, None),
                 wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = board
        self.move = move
        self.wins = wins
        self.visits = visits
        self.children = children or []
        self.parent = None
        self.untried_moves = logic.get_possible_moves(board)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class Random(PlayerStrat):
    # Build here the class for a random player
    def start(self):
        # Get all possible moves
        possible_moves = logic.get_possible_moves(self.root_state)
        # Select a random move
        move = random.choice(possible_moves)
        return move
    

class MiniMax(PlayerStrat):
    # Build here the class implementing the MiniMax strategy
    def start(self):
        
        best_move = None
        best_score = -inf

        score, move = self.minmax(self.root_state, 3, True)


        print("Score: ", score)
        print("Move: ", best_move)

        return best_move
    
    def minmax(self, board, depth, is_maximizing):
        """
        @return the score of the board state for the player and the move to play

        Minmax algorithm
        """
        # Check if game is over
        winner = logic.is_game_over(self.player, board)
        if winner or depth == 0:
            return self.evaluate(winner), board
        
        if is_maximizing:
            value = -inf
            for move in logic.get_possible_moves(board):
                copy_board = copy.deepcopy(board) 
                copy_board[move] = self.player  # Update copy_board with move
            
                result_val, new_board = self.minmax(copy_board, depth-1, False)
                if result_val > value:
                    value = result_val
                    board = new_board
                copy_board = None
        else:
            value = inf
            for move in logic.get_possible_moves(board):
                copy_board = copy.deepcopy(board)
                copy_board[move] = self.player-1  # Update copy_board with move

                result_val, new_board = self.minmax(copy_board, depth-1, True)
                if result_val < value:
                    value = result_val
                    board = new_board
                copy_board = None
        return value, board
    
    def evaluate(self, winner):
        """
        @return 1 if the player won, -1 if the player lost, 0 otherwise

        Evaluate the board state for the player
        """
        if winner == self.player:
            return 1  # Player wins
        elif winner == None:
            return random.uniform(-0.9, 0.9)
        else:
            return -1 # Player loses

        
str2strat: dict[str, PlayerStrat] = {
        "human": None,
        "random": Random,
        "minimax": MiniMax,
}