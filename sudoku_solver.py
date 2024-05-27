import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import ImageGrab
import random
import time
import os

root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("700x800")
root.configure(bg='#f2f2f2')

entries = [[None for _ in range(9)] for _ in range(9)]


font = ('Arial', 18)
bg_color ='white'
selected_color = '#d1e7dd'
highlight_color = '#f8d7da'
border_color = '#bbbbbb'
button_bg = '#4CAF50 '
button_fg = '#ffffff'
button_active_bg = '#45a049'



def create_grid():
    for row in range(9):
        for col in range(9):
            if (col +1) % 3 == 0 and col!= 8:
                pad_x = (0,10)
            else:
                pad_x = (0,0)
            if (row +1) % 3 == 0 and row !=8:
                pad_y = (0,10)
            else:
                pad_y = (0,0)
            entry = tk.Entry(root, width = 3, font =('Arial',24), justify = 'center', bg=bg_color, relief='solid', bd=1,highlightbackground=border_color, highlightthickness=0, state=tk.NORMAL)
            entry.grid(row=row +1, column=col, padx=pad_x, pady=pad_y)
            entries[row][col] = entry
            




def is_valid(board,row,col,num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3* (col // 3) 
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def solve_board (board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1,10):
                    if is_valid(board,row,col,num):
                        board[row][col] = num
                        if solve_board(board):
                            return  True
                        board[row][col] = 0
                return False
    return True


def get_board():
    board = []
    for row in range (9):
        board_row = []
        for col in range(9):
            val =  entries[row][col].get()
            if val == '':
                board_row.append(0)
            else:
                board_row.append(int(val))
        board.append(board_row)
    return board


def set_board(board):
    for row in range(9):
        for col in range(9):
            entries[row][col].delete(0, tk.END)
            if board[row][col] != 0:
                  entries[row][col].insert(0, str(board[row][col]))


def highlight_invalid_entries(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] !=0 and not is_valid(board,row,col,board[row][col]):
                entries[row][col].config(bg='red')
            else:
                entries[row][col].config(bg=bg_color)


def solve_sudoku():
    board = get_board()
    if solve_board(board):
        set_board(board)
        save_puzzle(board)
    else:
        messagebox.showinfo("Sudoku Solver", "No solution exists for this Sudoku puzzle")
    highlight_invalid_entries(get_board())


def clear_grid():
    for row in range(9):
        for col in  range(9):
            entries[row][col].delete(0, tk.END) 
            entries[row][col].config(bg=bg_color)
    reset_timer()


def generate_puzzle(difficulty):
    clear_grid()
    base = 3
    side = base * base

    def pattern (r,c): return (base * ( r % base) + r // base + c) % side
    def shuffle ( s): return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in  shuffle(rBase) ]
    cols = [ g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1,base * base +1))

    board = [[nums[pattern(r,c)] for c in cols] for r in rows]
    
    squares = side * side
    empties = squares * difficulty// 100
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    set_board(board)


def set_difficulty(level):
    if level == 'Easy':
        generate_puzzle(41)
    elif level == 'Medium':
        generate_puzzle(51)
    elif level == 'Hard':
        generate_puzzle(66)


screenshot_counter = 0
def take_screenshot():
    global screenshot_counter
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    x1 = x + root.winfo_width()
    y1 = y + root.winfo_height()
    filename = f"sudoku_screenshot_{screenshot_counter}.png"
    ImageGrab.grab().crop((x,y,x1,y1)).save(filename)
    screenshot_counter += 1
messagebox.showinfo("Sudoku Solver", "Screenshot saved as {filename}")


def show_rules():
    rules_window = tk.Toplevel(root)
    rules_window.title("Sudoku Rules")
    rules_window.geometry("400x250")
    rules_text = (
        "Sudoku Rules:\n\n"
        "1. Each row must contain the digits 1 to 9 without repetition.\n"
        "2. Each column must contain the digits 1 to 9 without repetition.\n"
        "3. Each 3x3 sub-grid must contain the digits 1 to 9 without repetition.\n\n"
        "To solve the puzzle, fill the empty cells such that all rows, columns, "
        "and 3x3 sub-grids contain all digits from 1 to 9."
    )
    label = tk.Label(rules_window, text=rules_text, justify=tk.LEFT, padx=10, pady=10)
    label.pack()


start_time = time.time()
timer_label = tk.Label(root,text="Time: 0s", font=('Arial',12),bg='#f2f2f2' )  
timer_label.grid(row=12,column=0,columnspan=9, pady=10)

def update_timer():
    elapsed_time =  int(time.time() - start_time)
    timer_label.config(text=f'Time: {elapsed_time}s')
    root.after(1000,update_timer)


def reset_timer():
    global start_time
    start_time = time.time()
    timer_label.config(text="Time: 0s")

def save_puzzle(board):
    try:
        file_path = os.path.join(os.getcwd(), "solved_puzzles.txt")
        with open(file_path, "a") as file:
            for row in board:
                file.write(" ".join(map(str, row)) + "\n")
            file.write("\n")  
        print(f"Puzzle saved successfully to {file_path}.")
        messagebox.showinfo("Sudoku Solver", f"Solved puzzle saved to solved_puzzles.txt.")
    except Exception as e:
        print(f"Error saving puzzle: {e}")
        messagebox.showerror("Sudoku Solver", f"Error saving puzzle: {e}")

def manual_save():
    board = get_board()
    save_puzzle(board)

create_grid()

button_frame = tk.Frame(root)
button_frame.grid(row=10,column=0,columnspan=9,pady=20)

solve_button = tk.Button(button_frame, text='Solve', command=solve_sudoku , width=10, font=('Arial',12))
solve_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text='Clear', command=clear_grid, width=10, font=('Arial',12))
clear_button.grid(row=0, column=1, padx=10 )

screenshot_button = tk.Button(button_frame,text='Screenshot', command=take_screenshot, width=10, font=('Arial',12))
screenshot_button.grid(row=0, column=2, padx=10)

rules_button = tk.Button(button_frame, text="Rules", command=show_rules, width=10, font=('Arial', 12))
rules_button.grid(row=0, column=3, padx=10)

save_button = tk.Button(button_frame, text="Save", command=manual_save, width=10, font=('Arial', 12))
save_button.grid(row=0, column=4, padx=10)

difficulty_frame = tk.Frame(root)
difficulty_frame.grid(row=11,column=0, columnspan=9, pady=10)
tk.Label(difficulty_frame, text='Select Difficulty:').pack(side=tk.LEFT)
tk.Button(difficulty_frame, text="Easy", command=lambda: set_difficulty('Easy')).pack(side=tk.LEFT)
tk.Button(difficulty_frame, text="Medium", command=lambda: set_difficulty('Medium')).pack(side=tk.LEFT)
tk.Button(difficulty_frame, text="Hard", command=lambda: set_difficulty('Hard')).pack(side=tk.LEFT)

update_timer()

root.mainloop()