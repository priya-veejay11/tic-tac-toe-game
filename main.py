import tkinter as tk
import random

root = tk.Tk()

root.title("Tic Tac Toe")
root.geometry("440x700")
root.configure(background="#111827")

title_label = tk.Label(
    root,
    text="TIC TAC TOE",
    font=("Segoe", 25, "bold"),
    bg="#111827",
    fg="#F9FAFB",
)
title_label.pack(pady=25)

subtitle_label = tk.Label(
    root,
    text="HUMAN VS. COMPUTER",
    font=("Segoe UI", 12, "bold"),
    bg="#111827",
    fg="#9CA3AF"
)
subtitle_label.pack(pady=1)

status_label = tk.Label(
    root,
    text="Your turn — X",
    font=("Segoe UI", 12, "bold"),
    bg="#111827",
    fg="#22D3EE"
)
status_label.pack(pady=15)

difficulty = tk.StringVar(value="Easy")

difficulty_frame = tk.Frame(
    root,
    bg="#111827"
)
difficulty_frame.pack(pady=5)

easy_button = tk.Radiobutton(
    difficulty_frame,
    text="Easy",
    variable=difficulty,
    value="Easy",
    font=("Segoe UI", 10, "bold"),
    bg="#0D9488",
    fg="#FFFFFF",
    selectcolor="#0F766E",
    indicatoron=0,
    width=10,
    pady=7
)
easy_button.pack(side="left", padx=5)

hard_button = tk.Radiobutton(
    difficulty_frame,
    text="Hard",
    variable=difficulty,
    value="Hard",
    font=("Segoe UI", 10, "bold"),
    bg="#7C3AED",
    fg="#FFFFFF",
    selectcolor="#5B21B6",
    indicatoron=0,
    width=10,
    pady=7
)
hard_button.pack(side="left", padx=5)


board_frame = tk.Frame(
    root,
    bg="#1F2937",
    padx=7,
    pady=7
)
board_frame.pack(pady=(25, 5))

buttons = []
board = [""] * 9
winning_lines = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]

game_over = False

def player_move(index):
    global game_over

    if game_over:
        return

    if board[index] == "":
        board[index] = "X"
        buttons[index].config(text='X', fg="#22D3EE")

        if check_winner() == "X":
            status_label.config(text="You win!", fg="#22D3EE")
            game_over = True
            return

        if check_draw():
            status_label.config(text="It's a draw!", fg="#F9FAFB")
            game_over = True
            return

        status_label.config(text="Computer is thinking...", fg="#A78BFA")
        root.after(350, computer_move)

def check_winner():
    for a,b,c in winning_lines:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    return None

def check_draw():
    if check_winner() is None and "" not in board:
        return True
    return False

def computer_move():
    global game_over
    available_moves = [index for index in range(9) if board[index] == ""]

    if not available_moves or game_over:
        return

    if difficulty.get() == "Easy":
        move = random.choice(available_moves)

    else:
        move = None

        # Priority 1: Check whether O can win
        for a, b, c in winning_lines:
            line = [board[a], board[b], board[c]]

            if line.count("O") == 2 and "" in line:
                for index in (a, b, c):
                    if board[index] == "":
                        move = index
                        break
                break

        # Priority 2: Block X from winning
        if move is None:
            for a, b, c in winning_lines:
                line = [board[a], board[b], board[c]]

                if line.count("X") == 2 and "" in line:
                    for index in (a, b, c):
                        if board[index] == "":
                            move = index
                            break
                    break

        # Priority 3: Choose a random empty cell
        if move is None:
            move = random.choice(available_moves)
    board[move] = "O"
    buttons[move].config(text="O", fg="#A78BFA")
    if check_winner() == "O":
        status_label.config(text="Computer wins!", fg="#A78BFA")
        game_over = True
        return

    if check_draw():
        status_label.config(text="It's a draw!", fg="#F9FAFB")
        game_over = True
        return

    status_label.config(text="Your turn — X", fg="#22D3EE")

def replay_game():
    global game_over

    board[:] = [""] * 9

    for button in buttons:
        button.config(text="")

    game_over = False
    status_label.config(text="Your turn — X", fg="#22D3EE")

for row in range(3):
    for col in range(3):
        index = row * 3 + col
        cell = tk.Button(
            board_frame,
            command=lambda i=index: player_move(i),
            text="",
            font=("Segoe", 32, "bold"),
            width=4,
            height=2,
            bg="#273449",
            fg="#F9FAFB",
            relief="flat",
        )
        cell.grid(row=row, column=col, padx=4, pady=4)
        buttons.append(cell)

replay_button = tk.Button(
    root,
    text="↻  Replay",
    command=replay_game,
    font=("Segoe UI", 8, "bold"),
    bg="#C4B5FD",
    fg="#312E81",
    activebackground="#A78BFA",
    activeforeground="#FFFFFF",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=7,
    pady=3
)
replay_button.place(relx=0.97, rely=0.025, anchor="ne")

root.mainloop()
