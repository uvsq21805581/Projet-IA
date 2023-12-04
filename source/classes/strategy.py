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
    def __init__(self, board, player=None, move=(None, None),
                 wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = copy.deepcopy(board)
        self.player = player
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
        
        self.root_node = Node(self.root_state, player=1)
        
        score, move = self.minmax()
        print("score and move: ", score, move)
        
        best_move = move
        best_score = score
        
        print("best move and score: ", best_move, best_score)
        # input("press enter to continue")
        return best_move
    
    def minmax(self, depth = inf):
        """
        @return the score of the board state for the player and the move to play

        Minmax algorithm
        """
        def max_value(node, depth, curr_player, inner_depth):
            value = self.utility(node)
            print("inner depth: ", inner_depth, "player: ", curr_player, "value: ", value)
            print("node state:\n", node.state)
            # input("press enter to continue")

            if inner_depth >= depth or value < 0: # revoir la condition avec un is game over
                print("Max depth: ", inner_depth, value)
                return value, node.move
            
            value = -np.inf
            action = None 
            actions = logic.get_possible_moves(node.state)
            nextPlayer = 1 if curr_player == 2 else 2
            for a in actions:
                x, y = a
                nextNode = Node(node.state, player = curr_player, move = a)
                nextNode.state[x][y] = curr_player
                nextNode.parent = node
                node.add_child(nextNode)

                v2, a2 = min_value(nextNode, depth, nextPlayer, inner_depth+1)
                if v2 > value:
                    value = v2 
                    action = a2
            return value, action

        def min_value(node, depth, curr_player, inner_depth):
            """
            @return the score of the board state for the player and the move to play
            """
            value = self.utility(node)
            print("inner depth: ", inner_depth, "player: ", curr_player, "value: ", value)
            print("node state:\n", node.state)
            # input("press enter to continue")

            if inner_depth >= depth or value is not None: # revoir la condition avec un is game over
                print("Min depth: ", inner_depth, value)
                return value, node.move
            
            value = np.inf
            action = None 
            actions = logic.get_possible_moves(node.state)
            nextPlayer = 1 if curr_player == 2 else 2
            for a in actions:
                x, y = a
                nextNode = Node(node.state, player = curr_player, move = a)
                nextNode.state[x][y] = curr_player
                nextNode.parent = node
                node.add_child(nextNode)
                v2, a2 = max_value(nextNode, depth, nextPlayer, inner_depth+1)
                if v2 < value :
                    value = v2 
                    action = a2
            return value, action

        self.root_node.player = self.player
        # print("INIT PLAYER", self.player)
        return max_value(self.root_node, depth, self.player, 0)
        
    def utility(self, node):
        res = logic.is_game_over(self.root_node.player, node.state)
        print("RES", res, "PLAYER", self.player, "NODE", node.state)

        if res == node.player:
            return 2
        else :
            return -1
        
str2strat: dict[str, PlayerStrat] = {
        "human": None,
        "random": Random,
        "minimax": MiniMax,
}