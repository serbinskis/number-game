import math
import random
import sys
import time
from typing import Optional
import game as game
from tree_visualizer import TreeNode

class GameAI:
    algorithms = { "Minimax": "_minimax_algorithm", "Alpha-Beta Pruning": "_alpha_beta_algorithm", "Random": "_random_algorithm" }

    def __init__(self, ui, game: "game.NumberGame", algorithm: str = None):
        self.ui = ui
        self.game = game
        self.algorithm = algorithm
        self.max_depth = 3
    
    def set_algorithm(self, algorithm: str):
        """Sets the AI algorithm to use."""
        if algorithm not in self.algorithms: raise ValueError(f"Invalid algorithm choice: {algorithm}")
        self.algorithm = algorithm

    def set_tree(self):
        self.tree = self

    def set_max_depth(self, max_depth: int = 3):
        """Sets the maximum depth for search algorithms."""
        self.max_depth = max_depth
    
    def get_max_depth(self) -> int:
        """Returns the max depth for search algorithms."""
        return self.max_depth 

    def next_move(self) -> int:
        """Determines the next move based on the selected algorithm."""
        if self.algorithm not in self.algorithms: raise ValueError(f"Unknown algorithm: {self.algorithm}")
        method_name = self.algorithms[self.algorithm]
        return getattr(self, method_name)()

    def _random_algorithm(self):
        """Randomly selects a valid divisor (2, 3, or 4)."""
        current_move = self.game.get_current_move()
        current_move.generate_children()
        return random.choice(current_move.children).divisor_number if current_move.children else None

    #TODO: Fix -> https://prnt.sc/sbo5Y-FNTE_z
    def _minimax_algorithm(self) -> int:
        def _minimax_score(node: "TreeNode"):
            is_game_over = (node.current_number <= 10) or not any(node.current_number % d == 0 for d in [2, 3, 4])
            if (is_game_over and (node.current_player == 1)): return -sys.maxsize
            return node.player_2_score

        def _minimax_helper(node: Optional["TreeNode"] = None, depth: int = 0) -> Optional["TreeNode"]:
            while (self.ui.rendering): time.sleep(0.0001)
            self.ui.tree.set_selected(node)
            time.sleep(2.000)
            while (self.ui.paused): time.sleep(0.0001)

            if (depth >= self.max_depth): return node
            node.generate_children()
            if (not node.children): return node
            best_node = max(node.children, key=lambda child: _minimax_score(_minimax_helper(child, depth + 1)), default=None)
            best_node.text = f" [BEST HIT ({_minimax_score(best_node)})]\n" + best_node.text
            return best_node

        best_node = _minimax_helper(self.game.get_current_move()) #best_node is one of the children, we must either remove it or set current move to it
        return best_node.divisor_number

    def _alpha_beta_algorithm(self):
        return self._random_algorithm()