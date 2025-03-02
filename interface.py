import threading
import time
from tkinter import Button, Canvas, Frame, Label, Tk
from game import NumberGame
from game_ai import GameAI
from tree_visualizer import TreeVizualizer


class GameInterface:
    def __init__(self, width: int, height: int):
        self.game = None
        self.tree = None
        self.window = Tk()
        self.width = width
        self.height = height
        self.rendering = False
        self.paused = False
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

        self.init_stage_choose_number()
        self.window.bind("<KeyPress>", lambda event: self.on_key_press(event))
        self.window.after(16, self.render)
        self.window.mainloop()

    def render(self, force: bool = False):
        self.window.after(16, self.render)
        if (not self.game or not self.game.started): return
        if (not force and self.rendering): return
        if (not force and time.time() - self.last_render_time) * 1000 < 16: return

        if (not force): self.rendering = True
        self.canvas.delete("all")
        if self.tree: self.tree.render(self.canvas)
        self.last_render_time = time.time()
        if (not force): self.rendering = False
    
    def clear_stage(self):
        for element in self.stage: element.destroy()
        label = Label(self.window, text="INFO: Use arrow keys to navigate the tree", font=("Arial", 12, "bold"), fg="blue") # Create an info label
        label.place(x=20, y=self.height - 40)  # Position it near the bottom of the window
        self.stage.append(label) # Store the label in the stage list so it can be removed later

    # Let user select generated number
    def init_stage_choose_number(self):
        self.clear_stage()

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
            button = Button(self.window, text=str(num), font=("Arial", 12), command=lambda n=num: self.init_stage_choose_who_starts(n))
            button_x = (window_width - button_width) // 2  # Center horizontally
            button_y = start_y + i * (button_height + button_spacing)  # Position with spacing
            button.place(x=button_x, y=button_y, width=button_width, height=button_height)
            self.stage.append(button)
    
    def init_stage_choose_who_starts(self, current_number):
        self.clear_stage()  # Remove previous UI elements

        # Get window dimensions
        window_width = self.width // 2
        window_height = self.height

        # Create label
        label = Label(self.window, text="Who starts the game?", font=("Arial", 14))
        label.update_idletasks()
        label_x = (window_width - label.winfo_reqwidth()) // 2
        label.place(x=label_x, y=window_height // 4)
        self.stage.append(label)

        # Create buttons for selecting Player or Computer
        button_width = 140
        button_height = 40
        button_spacing = 20
        start_y = (window_height // 3)

        for i, (text, player) in enumerate([("Player", 1), ("Computer", 2)]):
            button = Button(self.window, text=text, font=("Arial", 14),  command=lambda p=player: self.init_stage_choose_algorithm(current_number, p))
            button_x = (window_width - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            button.place(x=button_x, y=button_y, width=button_width, height=button_height)
            self.stage.append(button)

    def init_stage_choose_algorithm(self, current_number, current_player):
        self.clear_stage()  # Remove previous UI elements

        # Get window dimensions
        window_width = self.width // 2
        window_height = self.height

        # Create label
        label = Label(self.window, text="Choose AI Algorithm:", font=("Arial", 14))
        label.update_idletasks()
        label_x = (window_width - label.winfo_reqwidth()) // 2
        label.place(x=label_x, y=window_height // 4)
        self.stage.append(label)

        button_width = 180
        button_height = 40
        button_spacing = 20
        start_y = (window_height // 3)

        for i, algo in enumerate(GameAI._algorithms.keys()):
            button = Button(self.window, text=algo, font=("Arial", 14), command=lambda a=algo: self.init_stage_choose_difficulty(current_number, current_player, a))
            button_x = (window_width - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            button.place(x=button_x, y=button_y, width=button_width, height=button_height)
            self.stage.append(button)

    def init_stage_choose_difficulty(self, current_number, current_player, algorithm):
        self.clear_stage()  # Remove previous UI elements

        window_width = self.width // 2
        window_height = self.height

        label = Label(self.window, text="Choose Difficulty:", font=("Arial", 14))
        label.update_idletasks()
        label_x = (window_width - label.winfo_reqwidth()) // 2
        label.place(x=label_x, y=window_height // 4)
        self.stage.append(label)

        button_width = 180
        button_height = 40
        button_spacing = 20
        start_y = (window_height // 3)

        for i, difficulty in enumerate(GameAI._difficulties.keys()):
            button = Button(self.window, text=difficulty, font=("Arial", 14), command=lambda d=difficulty: self.start_game(current_player, current_number, algorithm, d))
            button_x = (window_width - button_width) // 2
            button_y = start_y + i * (button_height + button_spacing)
            button.place(x=button_x, y=button_y, width=button_width, height=button_height)
            self.stage.append(button)

    def init_stage_make_move(self):
        self.clear_stage()  # Remove previous UI elements
        if (self.game.get_current_player() == 2):
            threading.Thread(target=self.apply_move, daemon=True).start()
            return

        # Get the current game state from self.game
        game_state = self.game.get_current_move()

        # Get window dimensions
        window_width = self.width // 2
        window_height = self.height

        # Create labels for Player 1, Player 2, and Bank Score
        label_bank = Label(self.window, text=f"Bank Score: {game_state.bank_score}", font=("Arial", 14))
        label_p1 = Label(self.window, text=f"Player Score {game_state.player_1_score}", font=("Arial", 14))
        label_p2 = Label(self.window, text=f"Computer Score: {game_state.player_2_score}", font=("Arial", 14))
        label_algorithm = Label(self.window, text=f"Algorithm: {self.game.ai.get_algorithm()}", font=("Arial", 14))
        label_difficulty = Label(self.window, text=f"Difficulty: {self.game.ai.get_difficulty()}", font=("Arial", 14))

        # Place labels
        label_bank.place(x=20, y=20)
        label_p1.place(x=20, y=60)
        label_p2.place(x=20, y=100)
        label_algorithm.place(x=20, y=140)
        label_difficulty.place(x=20, y=180)

        # Store UI elements for later removal
        self.stage.extend([label_p1, label_p2, label_bank, label_algorithm, label_difficulty])

        # Display the Current Number
        label_number = Label(self.window, text=f"Current Number: {game_state.current_number}", font=("Arial", 16, "bold"))
        label_number.update_idletasks()
        label_x = (window_width - label_number.winfo_reqwidth()) // 2
        label_number.place(x=label_x, y=window_height // 2.5)
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
    
    def init_stage_game_over(self):
        self.clear_stage()  # Remove previous UI elements

        # Get the final game state
        game_state = self.game.get_current_move()

        # Determine the winner
        if game_state.player_1_score > game_state.player_2_score:
            winner_text = "Player Wins!"
        elif game_state.player_1_score < game_state.player_2_score:
            winner_text = "Computer Wins!"
        else:
            winner_text = "It's a Tie!"

        # Get window dimensions
        window_width = self.width // 2
        window_height = self.height

        # Display Winner Label
        label_winner = Label(self.window, text=winner_text, font=("Arial", 16, "bold"))
        label_winner.update_idletasks()
        label_x = (window_width - label_winner.winfo_reqwidth()) // 2
        label_winner.place(x=label_x, y=window_height // 4)
        self.stage.append(label_winner)

        # Display Scores (Centered)
        scores_text = f"Player Score: {game_state.player_1_score}\nComputer Score: {game_state.player_2_score}"
        label_scores = Label(self.window, text=scores_text, font=("Arial", 14), justify="center")
        label_scores.update_idletasks()
        scores_x = (window_width - label_scores.winfo_reqwidth()) // 2
        label_scores.place(x=scores_x, y=window_height // 2 - 40)
        self.stage.append(label_scores)

        # Restart Button
        button_restart = Button(self.window, text="Restart", font=("Arial", 14), command=self.init_stage_choose_number)
        button_x = (window_width - 120) // 2
        button_y = window_height - 100
        button_restart.place(x=button_x, y=button_y, width=120, height=40)
        self.stage.append(button_restart)

    def on_key_press(self, event):
        if (not self.game or not self.game.started): return
        if (event.keysym == "space"): self.paused = not self.paused
        if (event.keysym == "Return"): self.tree.set_selected(self.game.get_current_move())
        #if (event.keysym == "BackSpace"): self.tree.selected_node.remove_children()
        self.tree.move_selected(event.keysym)  # Move the selected node based on the arrow key

    def start_game(self, current_player: int, current_number: int, algorithm: str, difficulty: str):
        self.game = NumberGame(self)
        self.game.set_algorithm(algorithm)
        self.game.set_difficulty(difficulty)
        self.game.start_game(current_player, current_number)
        self.tree = TreeVizualizer(self.game.root)
        self.init_stage_make_move()

    def apply_move(self, divisor: int = -1):
        self.window.after(0, self.clear_stage)
        current_player = self.game.get_current_player()
        if (current_player == 2): self.game.ai_next_move()
        if (current_player == 1): self.game.next_move(divisor)
        while (self.rendering): time.sleep(0.0001)
        self.tree.set_selected(self.game.get_current_move())
        if (not self.game.is_finished()): self.window.after(0, self.init_stage_make_move)
        if (self.game.is_finished()): self.window.after(0, self.init_stage_game_over)