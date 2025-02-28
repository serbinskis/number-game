import game as game

class GameAI:
    def __init__(self, game: "game.NumberGame", algorithm: str = None):
        self.game = game
        self.algorithm = algorithm
    
    def set_algorithm(self, algorithm: str):
        self.algorithm = algorithm

    def next_move(self) -> int:
        if (self.game.get_current_move().current_number % 2 == 0): return 2
        if (self.game.get_current_move().current_number % 3 == 0): return 3
        if (self.game.get_current_move().current_number % 4 == 0): return 4
    
    #TODO: Implement Algorithms
        