import random
from game_ai import GameAI
from tree_visualizer import TreeNode
from tkinter import *

class GameStateNode(TreeNode):
    def __init__(self, current_number, divisor_number, current_player, player_1_score, player_2_score, bank_score):
        self.current_number = current_number 
        self.divisor_number = divisor_number 
        self.current_player = current_player # Current player (1 or 2)
        self.player_1_score = player_1_score # Score of Player 1
        self.player_2_score = player_2_score # Score of Player 2
        self.bank_score = bank_score # Bank points
        super().__init__(str(self))
    
    def __str__(self):
        return f'SCORE: {self.current_number}\nDIVISOR: {self.divisor_number}\nBANK: {self.bank_score}\nCOMPUTER SCORE: {self.player_2_score}\nPLAYER SCORE: {self.player_1_score}\n\n\n'

    def get_fill_color(self):
        if self.is_selected(): return "#ffcc00"
        if self.parent is None: return self.fill_color
        if self.current_player == 2: return "#00ff00" # Yes they are flipped
        if self.current_player == 1: return "#ff0000" # The current_player, state of who is playing now
        return self.fill_color

    def is_game_over(self) -> bool:
        return (self.current_number <= 10) or not any(self.current_number % d == 0 for d in [2, 3, 4])
    
    def heuristic_score(self) -> int:
        return self.player_2_score - self.player_1_score

    def generate_children(self, divisors=[2, 3, 4], recursive=False):
        for divisor in divisors:
            if (self.current_number % divisor == 0):  # Ensure division results in an integer
                new_value = self.current_number // divisor
                new_score1, new_score2, new_bank = self.player_1_score, self.player_2_score, self.bank_score

                # Apply scoring rules
                if new_value % 2 == 0:
                    if self.current_player == 1:
                        new_score1 -= 1
                    else:
                        new_score2 -= 1
                else:
                    if self.current_player == 1:
                        new_score1 += 1
                    else:
                        new_score2 += 1

                # Bank points condition
                if (new_value % 10 == 0 or new_value % 10 == 5): new_bank += 1
                is_game_over = (new_value <= 10) or not any(new_value % d == 0 for d in [2, 3, 4])

                if is_game_over:
                    # Add bank points to the current player's score
                    if self.current_player == 1:
                        new_score1 += new_bank
                    else:
                        new_score2 += new_bank
                    new_bank = 0  # Reset the bank as it has been claimed

                # Create child node with updated values and switch player
                child_node = GameStateNode(new_value, divisor, (2 if self.current_player == 1 else 1), new_score1, new_score2, new_bank)
                self.add_children(child_node=child_node)
                if (recursive): child_node.generate_children(divisors=divisors, recursive=True)
    

class NumberGame:
    def __init__(self, ui):
        """Initialize the game with a random valid starting number."""
        self.started = False
        self.finished = False
        self.ai = GameAI(ui, self)

    def generate_valid_numbers(count=5, lower=20000, upper=30000):
        """Generate a list of unique numbers divisible by 2, 3, and 4 within a range."""
        numbers = set()
        while len(numbers) < count:
            num = random.randint(lower, upper)
            if (num % 2 == 0 and num % 3 == 0 and num % 4 == 0): numbers.add(num)
        return list(numbers)

    def start_game(self, current_player, current_number):
        if self.started: return False
        self.root = GameStateNode(current_number, 0, current_player, 0, 0, 0)
        self.current_move = self.root
        self.started = True
        return self.started
    
    def next_move(self, selected_number):
        if self.is_finished() or not self.started: return False
        self.current_move.generate_children(divisors=[selected_number])
        self.current_move = self.current_move.children[0]

    def set_next_move(self, selected_number):
        if self.is_finished() or not self.started: return False
        for child in self.current_move.children:
            if child.divisor_number == selected_number: self.current_move = child
        self.current_move.remove_children()

    def get_current_move(self) -> "GameStateNode":
        return self.current_move

    def get_current_player(self) -> int:
        return self.get_current_move().current_player

    def get_current_number(self) -> int:
        return self.get_current_move().current_number
    
    def set_algorithm(self, algorithm: str):
        self.ai.set_algorithm(algorithm)

    def set_difficulty(self, difficulty: str):
        self.ai.set_difficulty(difficulty)
    
    def ai_next_move(self):
        current_move = self.current_move
        next_move = self.ai.next_move()
        self.current_move = current_move
        self.set_next_move(next_move)
    
    def is_finished(self):
        if self.finished: return True
        if (not self.get_current_move().is_game_over()): return False
        self.finished = True
        return self.finished