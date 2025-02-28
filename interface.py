import time
from tkinter import Button, Canvas, Frame, Label, Tk
from game import NumberGame
from tree_visualizer import TreeVizualizer


class GameInterface:
    def __init__(self, width: int, height: int):
        self.game = None
        self.tree = None
        self.window = Tk()
        self.width = width
        self.height = height
        self.rendering = False
        self.last_render_time = 0
        self.stage = []
 
    def start(self):
        self.window.title("Ciparu Spēle")  # Set the title
        self.window.resizable(False, False)  # Make it unresizable
        self.window.geometry(f"{self.width}x{self.height}+{(self.window.winfo_screenwidth() - self.width)//2}+{(self.window.winfo_screenheight() - self.height)//2}")
        self.canvas = Canvas(self.window, bg="white", height=self.height, width=self.width//2)
        self.canvas.place(x=self.width//2, y=-1)
        self.canvas.delete("all")

        frame = Frame(self.window, width=4, height=self.height, bg="black")
        frame.place(x=(self.width//2)-2, y=0)

        self.init_stage_1()
        self.window.bind("<KeyPress>", lambda event: self.on_key_press(event))
        self.window.after(16, self.render)
        self.window.mainloop()

    def render(self):
        self.window.after(16, self.render)
        if (not self.game or not self.game.started or self.rendering): return
        if (time.time() - self.last_render_time) * 1000 < 16: return

        self.rendering = True
        self.canvas.delete("all")
        if self.tree: self.tree.render(self.canvas)
        self.last_render_time = time.time()
        self.rendering = False
    
    def clear_stage(self):
        for element in self.stage: element.destroy()

    def init_stage_1(self):
        # Get window dimensions
        window_width = self.width // 2
        window_height = self.height

        # Create label
        label = Label(self.window, text="Choose a starting number:", font=("Arial", 14))
        label.update_idletasks()  # Ensure size calculation before placing
        label_width = label.winfo_reqwidth()
        label_x = (window_width - label_width) // 2  # Center horizontally
        label.place(x=label_x, y=window_height // 4)  # Place label at 1/4th of the height
        self.stage.append(label)

        # Generate 5 valid numbers for buttons
        start_numbers = NumberGame.generate_valid_numbers(count=5)
        button_width = 120
        button_height = 30
        button_spacing = 10
        total_button_height = len(start_numbers) * (button_height + button_spacing)

        start_y = (window_height // 2) - (total_button_height // 2)  # Center vertically

        # Create buttons dynamically
        for i, num in enumerate(start_numbers):
            button = Button(self.window, text=str(num), font=("Arial", 12), command=lambda n=num: self.start_game(n))
            button_x = (window_width - button_width) // 2  # Center horizontally
            button_y = start_y + i * (button_height + button_spacing)  # Position with spacing
            button.place(x=button_x, y=button_y, width=button_width, height=button_height)
            self.stage.append(button)

    def init_stage_2(self):
        self.clear_stage()  # Remove previous UI elements

        # Get the current game state from self.game
        game_state = self.game.get_current_move()

        # Get window dimensions
        window_width = self.width // 2
        window_height = self.height

        # Create labels for Player 1, Player 2, and Bank Score
        label_p1 = Label(self.window, text=f"Player 1 Score: {game_state.player_1_score}", font=("Arial", 14))
        label_p2 = Label(self.window, text=f"Player 2 Score: {game_state.player_2_score}", font=("Arial", 14))
        label_bank = Label(self.window, text=f"Bank Score: {game_state.bank_score}", font=("Arial", 14))

        # Place labels
        label_p1.place(x=20, y=20)
        label_p2.place(x=20, y=60)
        label_bank.place(x=20, y=100)

        # Store UI elements for later removal
        self.stage.extend([label_p1, label_p2, label_bank])

        # Display the Current Number
        label_number = Label(self.window, text=f"Current Number: {game_state.current_number}", font=("Arial", 16, "bold"))
        label_number.update_idletasks()
        label_x = (window_width - label_number.winfo_reqwidth()) // 2
        label_number.place(x=label_x, y=window_height // 4)
        self.stage.append(label_number)

        # Create buttons for dividing by 2, 3, 4
        button_width = 120
        button_height = 40
        button_spacing = 20
        start_y = (window_height // 2)

        for i, divisor in enumerate([2, 3, 4]):
            is_valid_move = (game_state.current_number % divisor == 0)  # Check divisibility
            button = Button(self.window, text=f"÷ {divisor}", font=("Arial", 14), command=lambda d=divisor: self.apply_move(d), state="normal" if is_valid_move else "disabled")
            button_x = (window_width - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            button.place(x=button_x, y=button_y, width=button_width, height=button_height)
            self.stage.append(button)
    
    def on_key_press(self, event):
        self.tree.move_selected(event.keysym)  # Move the selected node based on the arrow key
    
    def start_game(self, number):
        self.game = NumberGame()
        self.game.start_game(1, number)
        #self.game.root.generate_children(divisors=[2,3,4], recursive=True)
        self.tree = TreeVizualizer(self.game.root)
        self.init_stage_2()

    def apply_move(self, divisor):
        self.game.next_move(divisor)
        self.tree.set_selected(self.game.get_current_move())
        self.init_stage_2()

if __name__ == '__main__':
    GameInterface(1200, 600).start()
    #tree.root.generate_children(divisors=[2,3,4], recursive=True)