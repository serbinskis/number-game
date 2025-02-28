import random
import game as game

class GameAI:
    algorithms = { "Minimax": "_minimax_algorithm", "Alpha-Beta Pruning": "_alpha_beta_algorithm", "Random": "_random_algorithm" }

    def __init__(self, game: "game.NumberGame", algorithm: str = None):
        self.game = game
        self.algorithm = algorithm
        self.max_depth = 3
    
    def set_algorithm(self, algorithm: str):
        """Sets the AI algorithm to use."""
        if algorithm not in self.algorithms: raise ValueError(f"Invalid algorithm choice: {algorithm}")
        self.algorithm = algorithm
            

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
        current_number = self.game.get_current_move().current_number
        valid_moves = [d for d in [2, 3, 4] if current_number % d == 0]
        return random.choice(valid_moves) if valid_moves else None
    
    def _minimax_algorithm(self):
        self._random_algorithm()

    def _alpha_beta_algorithm(self):
        self._random_algorithm()