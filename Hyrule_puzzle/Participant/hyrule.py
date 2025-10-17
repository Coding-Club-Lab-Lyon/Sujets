#!/usr/bin/env python3

from graphics.link import link_gui, fail
from typing import List
import argparse

Board = List[List[int]]


def parse_map(path: str):
    """
    Parse a 9x9 map file.
    Return the board (list of 9 lists of ints)
    False on any format error
    """

    # Open file
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() != ""]
    except Exception:
        return False

    if len(lines) != 9:
        return False

    board = []
    for line in lines:
        parts = line.split()
        if len(parts) != 9:
            return False
        row = []
        for p in parts:
            if not p.isdigit():
                return False
            n = int(p)
            if not (0 <= n <= 9):
                return False
            row.append(n)
        board.append(row)

    return board


def is_valid(b: Board, r: int, c: int, val: int) -> bool:
    """
    Check if the variable 'val' can go to the position (r, c)
    without going against the rule of Sudoku
    """
    if any(b[r][j] == val for j in range(9)):
        return False
    if any(b[i][c] == val for i in range(9)):
        return False
    # Vérifie le bloc 3x3 contenant (r, c)
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if b[i][j] == val:
                return False
    return True


# ------------------------------------------
# Algorithm - To implement
# ------------------------------------------
def hyrule_solver(board: Board) -> bool:
    """
    Implement the algorithm with recursive backtracking solver.
    Returns True if a solution is found (and modifies the board)
    False otherwise.
    """
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solve the Sudoku puzzle provided as an argument."
    )
    parser.add_argument(
        "--map",
        help="Effectuer une validation croisée"
    )
    args = parser.parse_args()

    if args.map:
        my_board = parse_map(args.map)
        if my_board is False:
            print("[!] The provided map is incorrect.")
            exit(1)
        if hyrule_solver(my_board) is False:
            fail()
            exit(1)
        link_gui(my_board)
    else:
        print("[!] Please provide the map path.")
        parser.print_help()
        exit(1)
