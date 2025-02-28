import math
import random
import sys
import time
from typing import Optional, Tuple
import game as game
from tree_visualizer import TreeNode

class GameAI:
    algorithms = { "Minimax": "_minimax_algorithm", "Maximax (Custom)": "_maximax_algorithm", "Alpha-Beta Pruning": "_alpha_beta_algorithm", "Random": "_random_algorithm" }

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

    #TODO: (WHY MINIMAX IS SO STUPID) -> https://prnt.sc/5D096zfvliCf
    #TODO: Rewrite, this is tottaly inccorect: https://www.youtube.com/watch?v=l-hh51ncgDI
    def _minimax_algorithm(self) -> int:
        def _minimax_score(node: "TreeNode"):
            is_game_over = (node.current_number <= 10) or not any(node.current_number % d == 0 for d in [2, 3, 4])
            if (is_game_over and (node.current_player == 2)): return -sys.maxsize//2
            return node.player_2_score

        def _minimax_helper(node: "TreeNode", depth: int, maximizingPlayer: bool) -> Tuple["TreeNode", int]:
            while (self.ui.rendering): time.sleep(0.0001) # Don't modify selected node while renderinbuuy7gyg
            self.ui.tree.set_selected(node) # Set selected node for algorithm vizulaization
            time.sleep(0.3) # Sleep for some time, so that renderer in main thread visualizes tree
            while (self.ui.paused): time.sleep(0.0001) # If paused wait infinitely

            is_game_over = (node.current_number <= 10) or not any(node.current_number % d == 0 for d in [2, 3, 4])
            if ((depth == 0) or is_game_over): return node, _minimax_score(node) 

            node.generate_children()  # Ensure children are created
            if (not node.children): return node, _minimax_score(node) # If no children, return score
            
            best_move = node.children[0] # Set callback to default node
            best_score = -sys.maxsize if maximizingPlayer else sys.maxsize

            if maximizingPlayer:
                for child in node.children:
                    eval_node, eval_score = _minimax_helper(child, depth - 1, False)
                    eval_node.add_extra_text(f" [HIT ({eval_score})]\n")
                    if (eval_score > best_score): best_move = eval_node
                    best_score = max(eval_score, best_score)
            else:
                for child in node.children:
                    eval_node, eval_score = _minimax_helper(child, depth - 1, True)
                    eval_node.add_extra_text(f" [HIT ({eval_score})]\n")
                    if (eval_score < best_score): best_move = eval_node
                    best_score = min(eval_score, best_score)

            best_move.add_extra_text(f"BEST")
            best_move = node if (depth != self.get_max_depth()) else best_move
            return best_move, best_score

        best_move, _ = _minimax_helper(self.game.get_current_move(), self.get_max_depth(), True)
        return best_move.divisor_number

    #TODO: Fix (I THINK ITS FIXED) -> https://prnt.sc/sbo5Y-FNTE_z
    def _maximax_algorithm(self) -> int:
        def _maximax_score(node: "TreeNode"):
            is_game_over = (node.current_number <= 10) or not any(node.current_number % d == 0 for d in [2, 3, 4])
            if (is_game_over and (node.current_player == 2)): return -sys.maxsize//2
            return node.player_2_score

        def _maximax_helper(node: Optional["TreeNode"] = None, depth: int = 0) -> Tuple["TreeNode", int]:
            while (self.ui.rendering): time.sleep(0.0001) # Don't modify selected node while renderinbuuy7gyg
            self.ui.tree.set_selected(node) # Set selected node for algorithm vizulaization
            time.sleep(0.3) # Sleep for some time, so that renderer in main thread visualizes tree
            while (self.ui.paused): time.sleep(0.0001) # If paused wait infinitely

            if (depth >= self.max_depth): return node, _maximax_score(node)
            node.generate_children()
            if (not node.children): return node, _maximax_score(node)

            children_scores = [(child, _maximax_helper(child, depth + 1)[1]) for child in node.children]
            best_node, best_score = max(children_scores, key=lambda x: x[1])
            [child.add_extra_text(f" [HIT ({score})]\n") for child, score in children_scores]
            best_node.add_extra_text("BEST | ")
            return best_node, best_score

        #best_node is one of the children, we must either remove it or set current move to it
        best_node, _ = _maximax_helper(self.game.get_current_move())
        return best_node.divisor_number

    def _alpha_beta_algorithm(self):
        return self._random_algorithm()