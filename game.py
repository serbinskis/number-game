import random
from tree_visualizer import TreeNode, TreeVizualizer
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
        return f'[SCORE: {self.current_number}]\n[BANK: {self.bank_score}]\n[DIV: {self.divisor_number}]\n[P1: {self.player_1_score}] [P2: {self.player_2_score}]'

    def get_fill_color(self):
        if self.is_selected(): return "#ffcc00"
        if self.current_player == 1: return "#00ff00"
        if self.current_player == 2: return "#ff0000"
        return self.fill_color

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
                if new_value % 10 == 0 or new_value % 10 == 5:
                    new_bank += 1

                # Create child node with updated values and switch player
                child_node = GameStateNode(new_value, divisor, (2 if self.current_player == 1 else 1), new_score1, new_score2, new_bank)
                self.add_children(child_node=child_node)
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

def on_key_press(event, tree: TreeVizualizer, canvas: Canvas):
    tree.move_selected(event.keysym)  # Move the selected node based on the arrow key
    canvas.delete("all")  # Clear the canvas
    tree.draw_selected(canvas)  # Redraw with the selected node highlighted

if __name__ == '__main__':
    tree = TreeVizualizer(GameStateNode(29952, 0, 1, 0, 0, 0))
    tree.root.generate_children(divisors=[2,3,4], recursive=True)
    tree.print_tree()
    print(tree.find_max_depth())
    tree.execute_on_depth(-1, lambda node: print(str(node)))
    print("======================================")
    node = tree.find_first_node_at_depth(depth=-1)
    print(node.siblings_count)
    print(node.next_sibling.siblings_count)

    width = 1200
    height = 600

    top = Tk()
    top.title("Ciparu Spēle")  # Set the title
    top.resizable(False, False)  # Make it unresizable
    top.geometry(f"{width}x{height}+{(top.winfo_screenwidth() - width)//2}+{(top.winfo_screenheight() - height)//2}")
    canvas = Canvas(top, bg="white", height=height, width=width//2)
    canvas.place(x=width//2, y=-1)
    canvas.delete("all")

    frame = Frame(top, width=4, height=height, bg="black")
    frame.place(x=(width//2)-2, y=0)

    top.bind("<KeyPress>", lambda event: on_key_press(event, tree, canvas))
    tree.draw_selected(canvas)
    top.mainloop()