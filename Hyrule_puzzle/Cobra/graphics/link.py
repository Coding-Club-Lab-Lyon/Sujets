import tkinter as tk
from typing import List

# 9x9 Sudoku Board
Board = List[List[int]]
# Pixel Size Cell TK
CELL = 50


def link_gui(board: Board):
    window = tk.Tk()
    window.title("Master Sword")
    window.resizable(False, False)

    # Create the base grid
    canvas = tk.Canvas(window, width=9*CELL, height=9*CELL, bg='white')
    canvas.pack()

    def draw():
        canvas.delete("all")
        for i in range(10):
            if i % 3 == 0:
                w = 3
            else:
                w = 1
            canvas.create_line(0, i * CELL, 9 * CELL, i * CELL, width=w)
            canvas.create_line(i * CELL, 0, i * CELL, 9 * CELL, width=w)

            # Put the number
            for r in range(9):
                for c in range(9):
                    cell = board[r][c]
                    if cell != 0:
                        x = c * CELL + CELL // 2
                        y = r * CELL + CELL // 2
                        canvas.create_text(
                            x,
                            y,
                            text=str(cell),
                            font=("Helvetica", 18)
                        )

    draw()
    window.mainloop()


def fail():
    """Show a small dialog saying 'He failed to do it'."""
    window = tk.Tk()
    window.title("Master Sword")

    window.resizable(False, False)
    tk.Label(
        window,
        text="Sudoku solver failed",
        font=("Helvetica", 14),
        padx=20, pady=10
    ).pack()
    tk.Button(
        window,
        text="OK",
        command=window.destroy
    ).pack(pady=(0, 10))
    window.grab_set()
    window.focus_set()
    window.mainloop()
