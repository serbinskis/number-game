import random
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

class GameStateNode:
    def __init__(self, current_number, current_player, player_1_score, player_2_score, bank_score, parent=None):
        self.current_number = current_number 
        self.current_player = current_player  # Current player (1 or 2)
        self.player_1_score = player_1_score  # Score of Player 1
        self.player_2_score = player_2_score  # Score of Player 2
        self.bank_score = bank_score  # Bank points
        self.parent = parent  # Parent node (previous state)
        if (self.parent == None): self.any_node = Node(str(self))
        if (self.parent != None): self.any_node = Node(str(self), parent=self.parent.any_node)
        self.children = []  # Possible next moves
    
    def __str__(self):
        return f'[P1: {self.player_1_score}][P2: {self.player_2_score}][NUM: {self.current_number}][BANK: {self.bank_score}]'

    def generate_children(self, divisors=[2, 3, 4], recursive=False):
        """Generate possible moves and create child nodes."""
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
                if new_value % 10 == 0 or new_value % 10 == 5:
                    new_bank += 1

                # Create child node with updated values and switch player
                child_node = GameStateNode(new_value, (2 if self.current_player == 1 else 1), new_score1, new_score2, new_bank, self)
                self.children.append(child_node)
                if (recursive): child_node.generate_children(divisors=divisors, recursive=True)
    

class NumberGame:
    def __init__(self):
        """Initialize the game with a random valid starting number."""
        self.starting_numbers = self.generate_valid_numbers(count=5)
        self.started = False
        self.finished = False

    def generate_valid_numbers(self, count=5, lower=20000, upper=30000):
        """Generate a list of unique numbers divisible by 2, 3, and 4 within a range."""
        numbers = set()
        while len(numbers) < count:
            num = random.randint(lower, upper)
            if (num % 2 == 0 and num % 3 == 0 and num % 4 == 0):
                numbers.add(num)
        return list(numbers)

    def get_starting_numbers(self):
        return self.starting_numbers

    def start_game(self, current_player, current_number):
        if self.started: return False
        self.root = GameStateNode(current_number, current_player, 0, 0, 0)
        self.current_move = self.root
        self.started = True
        return self.started
    
    def next_move(self, selected_number):
        if self.is_finished() or not self.started: return False
        self.current_move.generate_children(divisors=[selected_number])
        self.current_move = self.current_move.children[0]
    
    def get_current_number(self):
        return self.current_move.current_number
    
    def is_finished(self):
        if self.finished: return True
        num = self.getCurrentNumber()
        if ((num > 10) and (num % 2 == 0 or num % 3 == 0 or num % 4 == 0)): return False
        self.finished = True
        return self.finished
    
    def draw_graph(self):
        if not self.started: return

        for pre, fill, node in RenderTree(self.root.any_node):
            print("%s%s" % (pre, node.name))
        
        #UniqueDotExporter(self.root.any_node).to_picture("NumberGame.png")

if __name__ == '__main__':
    number_game = NumberGame()
    print(number_game.get_starting_numbers())
    number_game.start_game(1, 29952)
    number_game.root.generate_children(divisors=[2, 3, 4], recursive=True)
    number_game.draw_graph()