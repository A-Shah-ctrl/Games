"""
Tic Tac Toe User Interface
"""
import tkinter as tk
from tkinter import ttk
from tictactoe import *

class StartScreen(tk.Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.grid_columnconfigure(j, weight=1)

        label = tk.Label(self, text="Choose A Mode", font=("Arial", 16), bg="black", fg="white")
        label.grid(row=1, column=0, columnspan=3, pady=10)
        ai_btn = tk.Button(self, text="One Player", command=lambda: window.start_game("ai"), bg="gray25", fg="white", relief="flat", activebackground="gray25", highlightthickness=2)
        ai_btn.grid(row=2, column=1, sticky="ew")
        human_btn = tk.Button(self, text="Two Player", command=lambda: window.start_game("human"),bg="gray25", fg="white", relief="flat", activebackground="gray25", highlightthickness=2)
        human_btn.grid(row=3, column=1, sticky="ew")

class GameScreen(tk.Frame):
    def __init__(self, window, mode):
        super().__init__(window, bg="black")
        self.window = window
        self.mode = mode # 'human' or 'ai'
        self.board = initial_state()
        self.current_turn = player(self.board)
        self.buttons = []

        for i in range(3):
            self.grid_columnconfigure(i)
        for i in range(6):
            self.grid_rowconfigure(i)

        for row in range(3):
            row_buttons = []
            for col in range(3):
                btn = tk.Button(self, text="", font=('Arial', 24), width=5, height=2,
                                bg="black", fg="white", activebackground="gray25",
                                command=lambda r=row, c=col: self.on_click(r, c))
                btn.grid(row=row, column=col)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.turn_label = tk.Label(self, text="{}'s turn".format(self.current_turn), bg="black", fg="white")
        self.turn_label.grid(row=4, column=0, columnspan=3, sticky="nsew")
        self.reset_button = tk.Button(self, text="Reset", bg="black", fg="white", command=lambda: self.window.start_game(self.mode))
        self.reset_button.grid(row=5, column=0, columnspan=1, sticky="nsew")
        self.reset_button = tk.Button(self, text="Quit", bg="black", fg="white", command=self.window.quit)
        self.reset_button.grid(row=5, column=2, columnspan=1, sticky="nsew")

    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    def enable_buttons(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] is None:
                    self.buttons[r][c].configure(state="normal")

    def on_click(self,r,c):
        if self.mode == "ai":
            self.disable_buttons()
        self.buttons[r][c].configure(text=self.current_turn, state="disabled")
        self.board = result(self.board, (r,c)) 
        over = terminal(self.board)
        if not over:
            self.current_turn = player(self.board)
            self.turn_label.configure(text="{}'s turn".format(self.current_turn),)
            if self.mode == "ai" and self.current_turn == "O":
                action = minimax(self.board)
                self.turn_label.configure(text="Hmmm.. let me think".format(self.current_turn))
                self.after(3000, lambda: self.pause(action))
        else:
            who_wins = winner(self.board)
            self.turn_label.configure(text="{} wins! Game over.".format(who_wins))  
            self.after(1000, self.window.quit) 
    
    def pause(self, action):
        self.buttons[action[0]][action[1]].configure(text=self.current_turn, state="disabled") 
        self.board = result(self.board, action) 
        self.enable_buttons()
        now_over = terminal(self.board)
        if not now_over:
            self.current_turn = player(self.board)
            self.turn_label.configure(text="{}'s turn".format(self.current_turn))
        else:
            who_wins = winner(self.board)
            self.turn_label.configure(text="{} wins! Game over.".format(who_wins))  
            self.after(1000, self.window.quit)  

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unbeatable Tic-Tac-Toe")
        self.geometry("315x350")
        self.resizable(False, False)
        self.frames = {}
        self.show_start_screen()

    def show_start_screen(self):
        self.frames["StartScreen"] = StartScreen(self)
        self.frames["StartScreen"].pack(fill="both", expand=True)
        self.frames["StartScreen"].tkraise()

    def start_game(self, mode: str):
        self.mode = mode
        if self.frames.get("StartScreen"):
            self.frames["StartScreen"].destroy()
        if self.frames.get("GameScreen"):
            self.frames["GameScreen"].destroy()
        self.frames["GameScreen"] = GameScreen(self, self.mode)
        self.frames["GameScreen"].pack(fill="both", expand=True)
        self.frames["GameScreen"].tkraise()


if __name__ == "__main__":
    game = TicTacToe()
    game.mainloop()