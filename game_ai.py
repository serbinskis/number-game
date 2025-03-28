import random
import sys
import time
from typing import Callable, Optional, Tuple
import game as game

class GameAI:
    _algorithms = { "Minimax": "_minimax_algorithm", "Alpha-Beta Pruning": "_alpha_beta_algorithm", "Maximax (Custom)": "_maximax_algorithm", "Random": "_random_algorithm" }
    _difficulties = { "Max": sys.maxsize, "Medium": 3, "Easy": 1 }
    _display_intervals = { "Max": 0.05, "Medium": 0.3, "Easy": 0.5 }

    def __init__(self, ui, game: "game.NumberGame", algorithm: str = None):
        self.ui = ui
        self.game = game
        self.algorithm = algorithm
        self.difficulty = "Medium"
        self.max_depth = 3
        self.sleep_interval = 0.3

    def get_algorithm(self) -> str:
        return self.algorithm

    def get_difficulty(self) -> str:
        return self.difficulty
    
    def set_algorithm(self, algorithm: str):
        """Sets the AI algorithm to use."""
        if algorithm not in self._algorithms: raise ValueError(f"Invalid algorithm choice: {algorithm}")
        self.algorithm = algorithm

    def set_difficulty(self, difficulty: str):
        """Sets the AI difficulty to use."""
        if difficulty not in self._difficulties: raise ValueError(f"Invalid difficulty choice: {difficulty}")
        self.difficulty = difficulty
        self.set_max_depth(self._difficulties[difficulty])
        self.sleep_interval = self._display_intervals[difficulty]

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
        if self.algorithm not in self._algorithms: raise ValueError(f"Unknown algorithm: {self.algorithm}")
        method_name = self._algorithms[self.algorithm]
        return getattr(self, method_name)()

    def _random_algorithm(self):
        """Randomly selects a valid divisor (2, 3, or 4)."""
        current_move: "game.GameStateNode" = self.game.get_current_move()
        current_move.generate_children()
        return random.choice(current_move.children).divisor_number if current_move.children else None

    #TODO: (DONE) Rewrite, this is tottaly inccorect: https://www.youtube.com/watch?v=l-hh51ncgDI
    def _minimax_algorithm(self) -> int:
        score_callback = game.GameStateNode.heuristic_score
        return self._minimax_helper(self.game.get_current_move(), self.get_max_depth(), score_callback=score_callback)[0].divisor_number

    #TODO: Fix (I THINK ITS FIXED) -> https://prnt.sc/sbo5Y-FNTE_z
    def _maximax_algorithm(self) -> int:
        score_callback = game.GameStateNode.heuristic_score
        return self._minimax_helper(self.game.get_current_move(), self.get_max_depth(), always_maximizing=True, score_callback=score_callback)[0].divisor_number

    def _alpha_beta_algorithm(self):
        score_callback = game.GameStateNode.heuristic_score
        return self._minimax_helper(self.game.get_current_move(), self.get_max_depth(), alpha=-sys.maxsize, beta=sys.maxsize, score_callback=score_callback)[0].divisor_number

    def _minimax_helper(self, node: "game.GameStateNode", depth: int, alpha: Optional[int] = None, beta: Optional[int] = None, maximizing: bool = True, always_maximizing: bool = False, score_callback: Callable[["game.GameStateNode"], None] = None) -> Tuple["game.GameStateNode", int]:
        while (self.ui.rendering): time.sleep(0.0001) # Don't modify selected node while rendering ui
        self.ui.tree.set_selected(node) # Set selected node for algorithm vizulaization
        time.sleep(self.sleep_interval) # Sleep for some time, so that renderer in main thread visualizes tree
        while (self.ui.paused): time.sleep(0.0001) # If paused wait infinitely

        if ((depth == 0) or node.is_game_over()): return node, score_callback(node) # If max depth reached, return score
        node.generate_children()  # Ensure children are created
        if (not node.children): return node, score_callback(node) # If no children, return score

        best_move = node.children[0] # Set callback to default node
        best_score = -sys.maxsize if (maximizing or always_maximizing) else sys.maxsize # We either compare to get max or min

        if (maximizing or always_maximizing): # Max or min score between all node's children
            for child in node.children:
                eval_node, eval_score = self._minimax_helper(child, depth - 1, alpha=alpha, beta=beta, maximizing=False, always_maximizing=always_maximizing, score_callback=score_callback)
                eval_node.add_extra_text(f" [EVAL ({eval_score})]\n")
                if (eval_score > best_score): best_move = eval_node
                best_score = max(eval_score, best_score)
                if ((beta is not None) and (alpha is not None)): alpha = max(alpha, eval_score)
                if ((beta is not None) and (alpha is not None) and (beta <= alpha)): break
        else:
            for child in node.children:
                eval_node, eval_score = self._minimax_helper(child, depth - 1, alpha=alpha, beta=beta, maximizing=True, always_maximizing=always_maximizing, score_callback=score_callback)
                eval_node.add_extra_text(f" [EVAL ({eval_score})]\n")
                if (eval_score < best_score): best_move = eval_node
                best_score = min(eval_score, best_score)
                if ((beta is not None) and (alpha is not None)): beta = min(beta, eval_score)
                if ((beta is not None) and (alpha is not None) and (beta <= alpha)): break

        # Don't return best_move, we need to return ourself, so that in the end we know which node leads to the best_move
        # If we cary the best_move from the bottom to the up, we will not know which of the root's nodes was the original
        # Since we replaced it with the best node from the bottom
        # Only in the end return best_move, since it will be the root's children with the best move
        # We don't want to return root, but one of it's children as the result

        best_move.add_extra_text(f"BEST")
        if (depth != self.get_max_depth()): best_move = node
        #best_move = node if (depth != self.get_max_depth()) else best_move
        return best_move, best_score