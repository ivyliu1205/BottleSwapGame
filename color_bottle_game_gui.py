import random
import tkinter as tk
from tkinter import messagebox, ttk

class ColorBottleGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Color Bottle Guessing Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Configure colors and styles
        self.root.configure(bg='#2c3e50')
        
        # Game state
        self.colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange']
        self.color_codes = {
            'Red': '#e74c3c',
            'Blue': '#3498db', 
            'Green': '#2ecc71',
            'Yellow': '#f1c40f',
            'Purple': '#9b59b6',
            'Orange': '#e67e22'
        }
        
        self.selected_positions = []
        self.bottle_buttons = []
        
        self.init_game()
        self.create_widgets()
        
    def init_game(self):
        """Initialize game state"""
        self.target_sequence = random.sample(self.colors, 5)
        self.current_sequence = self.target_sequence.copy()
        random.shuffle(self.current_sequence)
        
        # Ensure starting position is different from target
        while self.current_sequence == self.target_sequence:
            random.shuffle(self.current_sequence)
        
        self.swap_count = 0
        self.right_count = self.get_right_count()
        self.game_won = False
        self.selected_positions = []
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🎮 Color Bottle Guessing Game 🎮",
            font=("Arial", 24, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Click two bottles to swap them. Find the correct arrangement!",
            font=("Arial", 14),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        instructions.pack(pady=10)
        
        # Game stats frame
        stats_frame = tk.Frame(self.root, bg='#2c3e50')
        stats_frame.pack(pady=10)
        
        self.swap_label = tk.Label(
            stats_frame,
            text=f"Swaps: {self.swap_count}",
            font=("Arial", 16, "bold"),
            fg='#e74c3c',
            bg='#2c3e50'
        )
        self.swap_label.pack(side=tk.LEFT, padx=20)
        
        self.status_label = tk.Label(
            stats_frame,
            text="Select two bottles to swap",
            font=("Arial", 16),
            fg='#f39c12',
            bg='#2c3e50'
        )
        self.status_label.pack(side=tk.LEFT, padx=20)

        self.hint_label = tk.Label(
            stats_frame,
            text=f"{self.right_count} bottles are at right position",
            font=("Arial", 16),
            fg='#f39c12',
            bg='#2c3e50'
        )
        self.hint_label.pack(side=tk.LEFT, padx=20)
        
        # Bottles frame
        bottles_frame = tk.Frame(self.root, bg='#2c3e50')
        bottles_frame.pack(pady=30)
        
        # Create bottle buttons
        self.create_bottle_buttons(bottles_frame)
        
        # Control buttons frame
        controls_frame = tk.Frame(self.root, bg='#2c3e50')
        controls_frame.pack(pady=20)
        
        # New game button
        new_game_btn = tk.Button(
            controls_frame,
            text="🔄 New Game",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_btn = tk.Button(
            controls_frame,
            text="❌ Quit",
            font=("Arial", 14, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.quit_game
        )
        quit_btn.pack(side=tk.LEFT, padx=10)
        
    def create_bottle_buttons(self, parent):
        """Create bottle buttons with colors"""
        self.bottle_buttons = []
        
        for i in range(5):
            color = self.current_sequence[i]
            
            # Frame for each bottle
            bottle_frame = tk.Frame(parent, bg='#2c3e50')
            bottle_frame.pack(side=tk.LEFT, padx=15)
            
            # Position label
            pos_label = tk.Label(
                bottle_frame,
                text=f"Position {i+1}",
                font=("Arial", 12, "bold"),
                fg='#ecf0f1',
                bg='#2c3e50'
            )
            pos_label.pack(pady=5)
            
            # Bottle button (circular)
            bottle_btn = tk.Button(
                bottle_frame,
                text=color,
                font=("Arial", 15, "bold"),
                # bg=self.color_codes[color],
                # activebackground=self.color_codes[color],
                fg=self.color_codes[color],
                width=8,
                height=4,
                relief='raised',
                bd=3,
                # highlightthickness=0,
                command=lambda idx=i: self.bottle_clicked(idx)
            )
            bottle_btn.pack(pady=5)
            
            self.bottle_buttons.append(bottle_btn)
            
    def bottle_clicked(self, position):
        """Handle bottle button clicks"""
        if position in self.selected_positions:
            # Deselect if already selected
            self.selected_positions.remove(position)
            self.update_bottle_appearance(position, selected=False)
        else:
            # Select bottle
            if len(self.selected_positions) < 2:
                self.selected_positions.append(position)
                self.update_bottle_appearance(position, selected=True)
                
                # If two bottles selected, perform swap
                if len(self.selected_positions) == 2:
                    self.root.after(500, self.perform_swap)  # Small delay for visual feedback
        
        self.update_status()
        
    def update_bottle_appearance(self, position, selected=False):
        """Update bottle button appearance based on selection"""
        button = self.bottle_buttons[position]
        if selected:
            button.configure(relief='sunken', bd=5)
        else:
            button.configure(relief='raised', bd=3)
            
    def perform_swap(self):
        """Perform the swap between selected bottles"""
        if len(self.selected_positions) == 2:
            pos1, pos2 = self.selected_positions
            
            # Swap in sequence
            self.current_sequence[pos1], self.current_sequence[pos2] = \
                self.current_sequence[pos2], self.current_sequence[pos1]
            
            # Update button colors and text
            color1, color2 = self.current_sequence[pos1], self.current_sequence[pos2]
            
            self.bottle_buttons[pos1].configure(
                text=color1,
                bg=self.color_codes[color1],
                activebackground=self.color_codes[color1],
                fg=self.color_codes[color1],
                activeforeground='white'
            )
            self.bottle_buttons[pos2].configure(
                text=color2,
                bg=self.color_codes[color2],
                activebackground=self.color_codes[color2],
                fg=self.color_codes[color2],
                activeforeground='white'
            )
            
            # Reset appearance
            self.update_bottle_appearance(pos1, selected=False)
            self.update_bottle_appearance(pos2, selected=False)
            
            # Update swap count
            self.swap_count += 1
            self.swap_label.configure(text=f"Swaps: {self.swap_count}")

            # Update correct count
            self.right_count = self.get_right_count()
            self.hint_label.configure(text=f"{self.right_count} bottles are at right position")
            
            # Clear selections
            self.selected_positions = []
            
            # Check for win
            self.check_win()
            
        self.update_status()
        
    def update_status(self):
        """Update status message"""
        if len(self.selected_positions) == 0:
            self.status_label.configure(text="Select two bottles to swap", fg='#f39c12')
        elif len(self.selected_positions) == 1:
            self.status_label.configure(text="Select another bottle to swap", fg='#3498db')
        else:
            self.status_label.configure(text="Swapping bottles...", fg='#e74c3c')
            
    def check_win(self):
        """Check if player has won"""
        if self.current_sequence == self.target_sequence:
            self.game_won = True
            
            # Performance message
            if self.swap_count <= 3:
                performance = "Amazing! You're a puzzle master! 🌟"
            elif self.swap_count <= 6:
                performance = "Great job! Well done! 👍"
            elif self.swap_count <= 10:
                performance = "Good work! Keep practicing! 👌"
            else:
                performance = "You did it! Try to beat your record! 💪"
            
            message = f"🎉 CONGRATULATIONS! 🎉\n\nYou solved the puzzle in {self.swap_count} swaps!\n\n{performance}"
            
            result = messagebox.askquestion(
                "You Won!",
                message + "\n\nWould you like to play again?",
                icon='question'
            )
            
            if result == 'yes':
                self.new_game()
            else:
                self.quit_game()
                
    def get_right_count(self) -> int:
        """Provide the count of bottles at correct positions"""
        correct_positions = []
        for i, (current, target) in enumerate(zip(self.current_sequence, self.target_sequence)):
            if current == target:
                correct_positions.append(i + 1)
        return len(correct_positions)
        
    def new_game(self):
        """Start a new game"""
        self.init_game()
        
        # Update all bottle buttons
        for i, button in enumerate(self.bottle_buttons):
            color = self.current_sequence[i]
            button.configure(
                text=color,
                bg=self.color_codes[color],
                fg=self.color_codes[color],
                relief='raised',
                bd=3
            )
        
        # Reset UI
        self.swap_label.configure(text=f"Swaps: {self.swap_count}")
        self.hint_label.configure(text=f"{self.right_count} bottles are at right position")

        self.update_status()
        
    def quit_game(self):
        """Quit the game"""
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.quit()
            
    def run(self):
        """Start the game"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()
