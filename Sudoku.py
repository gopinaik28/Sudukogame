import tkinter as tk
from tkinter import messagebox
import random
import time

BOARD_SIZE = 9
BOX_SIZE = 3
EMPTY = 0

# --- Core Sudoku Logic ---
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(BOARD_SIZE)]:
        return False
    start_row, start_col = row - row % BOX_SIZE, col - col % BOX_SIZE
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def fill_box(board, row_start, col_start):
    nums = list(range(1, 10))
    random.shuffle(nums)
    idx = 0
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            board[row_start + i][col_start + j] = nums[idx]
            idx += 1

def fill_diagonal_boxes(board):
    for i in range(0, BOARD_SIZE, BOX_SIZE):
        fill_box(board, i, i)

def remove_cells(board, num_holes):
    count = 0
    while count < num_holes:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            count += 1

def generate_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    fill_diagonal_boxes(board)
    solve_sudoku(board)
    solution = [row[:] for row in board]
    remove_cells(board, 40)
    return board, solution

# --- GUI Class ---
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.entries = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board, self.solution = generate_board()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.draw_grid()

        # Buttons Frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        self.check_button = tk.Button(buttons_frame, text="Check", font=('Arial', 14), command=self.check_solution)
        self.check_button.pack(side='left', padx=10)

        self.pause_button = tk.Button(buttons_frame, text="Pause", font=('Arial', 14), command=self.pause_game)
        self.pause_button.pack(side='left', padx=10)

        # Timer variables
        self.start_time = time.time()
        self.paused = False
        self.pause_start_time = None
        self.total_paused_time = 0

    def draw_grid(self):
        for i in range(BOX_SIZE):
            self.main_frame.rowconfigure(i, weight=1)
            for j in range(BOX_SIZE):
                self.main_frame.columnconfigure(j, weight=1)
                box_frame = tk.Frame(self.main_frame, bg="black", borderwidth=2, relief='groove')
                box_frame.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                box_frame.rowconfigure(tuple(range(BOX_SIZE)), weight=1)
                box_frame.columnconfigure(tuple(range(BOX_SIZE)), weight=1)

                for m in range(BOX_SIZE):
                    for n in range(BOX_SIZE):
                        global_row = i * BOX_SIZE + m
                        global_col = j * BOX_SIZE + n
                        entry = tk.Entry(box_frame, font=('Arial', 16), justify='center', relief='flat')
                        entry.grid(row=m, column=n, sticky='nsew', padx=1, pady=1)

                        if self.board[global_row][global_col] != EMPTY:
                            entry.insert(0, str(self.board[global_row][global_col]))
                            entry.config(state='disabled', disabledforeground='black')

                        self.entries[global_row][global_col] = entry

    def check_solution(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                val = self.entries[i][j].get()
                if val.isdigit() and int(val) == self.solution[i][j]:
                    continue
                else:
                    messagebox.showerror("Sudoku", "Incorrect solution!")
                    return

        # If correct, calculate elapsed time
        elapsed_time = time.time() - self.start_time - self.total_paused_time
        mins, secs = divmod(int(elapsed_time), 60)
        time_str = f"{mins} minute(s) and {secs} second(s)"

        popup = tk.Toplevel(self.root)
        popup.title("Congratulations!")
        popup.geometry("350x180")
        popup.transient(self.root)
        popup.grab_set()
        popup.resizable(False, False)

        label = tk.Label(popup, text=f"🎉 You solved the puzzle in {time_str}!\nWhat would you like to do next?", font=('Arial', 12), justify='center')
        label.pack(pady=20)

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10)

        def start_new_game():
            popup.destroy()
            self.next_level()

        def exit_game():
            self.root.destroy()

        tk.Button(btn_frame, text="New Game", width=12, font=('Arial', 10), command=start_new_game).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Exit", width=12, font=('Arial', 10), command=exit_game).grid(row=0, column=1, padx=10)

    def next_level(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                entry = self.entries[i][j]
                entry.config(state='normal')
                entry.delete(0, tk.END)

        self.board, self.solution = generate_board()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] != EMPTY:
                    self.entries[i][j].insert(0, str(self.board[i][j]))
                    self.entries[i][j].config(state='disabled', disabledforeground='black')
                else:
                    self.entries[i][j].config(state='normal')

        self.start_time = time.time()
        self.total_paused_time = 0
        self.paused = False
        self.pause_start_time = None

    def pause_game(self):
        if not self.paused:
            self.paused = True
            self.pause_start_time = time.time()
            self.set_entries_state('disabled')
            self.check_button.config(state='disabled')
            self.pause_button.config(text='Resume')
            self.show_pause_popup()
        else:
            self.paused = False
            paused_duration = time.time() - self.pause_start_time
            self.total_paused_time += paused_duration
            self.pause_start_time = None
            self.set_entries_state('normal')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] != EMPTY:
                        self.entries[i][j].config(state='disabled')
            self.check_button.config(state='normal')
            self.pause_button.config(text='Pause')

    def set_entries_state(self, state):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == EMPTY:
                    self.entries[i][j].config(state=state)

    def show_pause_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Game Paused")
        popup.geometry("300x150")
        popup.transient(self.root)
        popup.grab_set()

        label = tk.Label(popup, text="Game is paused.\nResume or Exit?", font=('Arial', 12))
        label.pack(pady=20)

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10)

        def resume():
            popup.destroy()
            self.pause_game()

        def exit_game():
            self.root.destroy()

        tk.Button(btn_frame, text="Resume", width=10, command=resume).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Exit", width=10, command=exit_game).pack(side='left', padx=10)

# --- Run GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x850")
    root.minsize(600, 650)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    SudokuGUI(root)
    root.mainloop()
