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
import time

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
    def __init__(self, _board_state, player):
        super().__init__(_board_state, player)

    def start(self):
        
        best_move = None
        best_score = -inf
        
        self.root_node = Node(self.root_state, player = self.player)
        #self.kernel = self.gkern(len(self.root_node.state), 1)
        # print(self.kernel)
        temp = time.time()
        score, move = self.minmax(4)
        # print("time: ", time.time() - temp)
        # print("score: ", score)
        
        best_move = move
        best_score = score
        
        return best_move
    
    def minmax(self, depth = math.inf):
        """
        @return the score of the board state for the player and the move to play
        Minmax algorithm
        """
        def max_value(node, depth, inner_depth, alpha, beta):
            """
            @return the score of the board state for the player and the move to play
            """
            player = self.player
            if (inner_depth >= depth ) or (logic.is_game_over(3 - player, node.state) is not None):
                value = self.utility(node)
                return value, node.move

            
            value = -np.inf
            action = None 
            actions = logic.get_possible_moves(node.state)
            for a in actions:
                x, y = a
                nextNode = Node(node.state, player = player, move = a)
                nextNode.state[x][y] = player
                nextNode.parent = node
                node.add_child(nextNode)

                v2, a2 = min_value(nextNode, depth, inner_depth+1, alpha, beta)
                
                if v2 > value:
                    value = v2 
                    action = a2
                    alpha = max(alpha, v2)
                if value >= beta:
                    return value, action
                               
            return value, action

        def min_value(node, depth, inner_depth, alpha, beta):
            """
            @return the score of the board state for the player and the move to play
            """
            player = 3 - self.player
            if (inner_depth >= depth ) or (logic.is_game_over(3 - player, node.state) is not None):
                value = self.utility(node)
                return value, node.move
            
            value = np.inf
            action = None 
            actions = logic.get_possible_moves(node.state)
            for a in actions:
                x, y = a
                nextNode = Node(node.state, player = player, move = a)
                nextNode.state[x][y] = player
                nextNode.parent = node
                node.add_child(nextNode)
                
                v2, a2 = max_value(nextNode, depth, inner_depth+1, alpha, beta)
               
                if v2 < value :
                    value = v2 
                    action = a2
                    beta = min(beta, value)
                if value <= alpha:
                    return value, action

            return value, action

        return max_value(self.root_node, depth, 0, -np.inf, np.inf)
        
    def utility(self, node):
        """
        @return the score of the board state for the player and the move to play
        """
        res = logic.is_game_over(node.player, node.state)
        if res != self.player: # logique inversée
            return 200
        else :
            return -200

class ABheur(MiniMax):

    def start(self):
    
        best_move = None
        best_score = -inf
        
        self.root_node = Node(self.root_state, player = self.player)
        self.kernel = self.gkern(len(self.root_node.state), 1)
        # print(self.kernel)
        temp = time.time()
        score, move = self.minmax()
        # print("time: ", time.time() - temp)
        # print("score: ", score)
        
        best_move = move
        best_score = score
        
        return best_move

    def minmax(self):
        """
        @return the score of the board state for the player and the move to play
        Minmax algorithm
        """
        
        depth = int(np.sqrt(len(self.root_node.state[np.where(self.root_node.state != 0)]) + 1))
        # print("DEPTH : ",  depth)
        

        def max_value(node, depth, inner_depth, alpha, beta):
            """
            @return the score of the board state for the player and the move to play
            """
            player = self.player
            if (logic.is_game_over(3 - player, node.state) is not None):
                value = self.utility(node)
                return value, node.move
            if inner_depth >= depth :
                value = self.eval(node, player)
                return value, node.move
            
            value = -np.inf
            action = None 
            actions = logic.get_possible_moves(node.state)
            for a in actions:
                x, y = a
                nextNode = Node(node.state, player = player, move = a)
                nextNode.state[x][y] = player
                nextNode.parent = node
                node.add_child(nextNode)

                v2, a2 = min_value(nextNode, depth, inner_depth+1, alpha, beta)
                
                if v2 > value:
                    value = v2 
                    action = a2
                    alpha = max(alpha, v2)
                if value >= beta:
                    return value, action
                            
            return value, action

        def min_value(node, depth, inner_depth, alpha, beta):
            """
            @return the score of the board state for the player and the move to play
            """
            player = 3 - self.player
            if (logic.is_game_over(3 - player, node.state) is not None):
                value = self.utility(node)
                return value, node.move
            if inner_depth >= depth :
                value = self.eval(node, player)
                return value, node.move
            
            
            value = np.inf
            action = None 
            actions = logic.get_possible_moves(node.state)
            for a in actions:
                x, y = a
                nextNode = Node(node.state, player = player, move = a)
                nextNode.state[x][y] = player
                nextNode.parent = node
                node.add_child(nextNode)
                
                v2, a2 = max_value(nextNode, depth, inner_depth+1, alpha, beta)
            
                if v2 < value :
                    value = v2 
                    action = a2
                    beta = min(beta, value)
                if value <= alpha:
                    return value, action

            return value, action

        return max_value(self.root_node, depth, 0, -np.inf, np.inf)
        
    def eval(self, node, curr_player):
        """
        @return the score of the board state for the player and the move to play
        """
        temp = node.state
        temp[np.where(temp == curr_player)] = -1
        score_board = np.sum(temp * self.kernel)
        return score_board

    def gkern(self, l=5, sig=1.):
        """
        creates gaussian kernel with side length `l` and a sigma of `sig`
        """
        ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
        gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
        kernel = np.outer(gauss, gauss)
        return kernel / np.sum(kernel)

str2strat: dict[str, PlayerStrat] = {
        "human": None,
        "random": Random,
        "minimax": MiniMax,
        "abheur" : ABheur,
}

