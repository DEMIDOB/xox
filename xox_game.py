from functools import partial

import tkinter as tk
from tkinter.messagebox import showinfo

import numpy as np

FIELD_VALUES = ["  ", "o", "x"]


class XoxTriedToChangeAlreadyOccupiedCellError(Exception):
    pass


class ShouldRestartTheGame(Exception):
    pass


class XoxGame:
    def __init__(self):
        self.field = np.zeros((3, 3), dtype=int)
        self.buttons: [tk.Button] = [None for _ in range(9)]

        self.current_player = -1
        self.player_status_won = [False, False]

        self.active = True

    def click(self, r, c):
        assert r in range(3) and c in range(3), f"Wrong grid indexing ({r}, {c})"
        assert self.active, "Attempt to play an inactive game"

        if self.field[r][c]:
            raise XoxTriedToChangeAlreadyOccupiedCellError()

        self.field[r][c] = self.current_player
        self.buttons[r * 3 + c]["text"] = FIELD_VALUES[self.current_player]

        if self.is_winner_here(r, c):
            self.active = False
            return self.current_player

        self.current_player = -self.current_player

    def is_winner_here(self, r, c):
        return abs(self.field.sum(axis=0)[c]) == 3 \
               or abs(self.field.sum(axis=1)[c]) == 3 \
               or (r == c and abs(self.field.trace()) == 3) \
               or (3 - r - 1 == c and abs(np.fliplr(self.field).trace()) == 3)

    def restart(self):
        self.field = np.zeros((3, 3), dtype=int)

        self.current_player = -1
        self.player_status_won = [False, False]

        self.active = True

        for r in range(3):
            for c in range(3):
                self.buttons[r * 3 + c]["text"] = FIELD_VALUES[self.field[r][c]]

    def draw(self, frame: tk.Frame, row_offset=0):
        def _click_command(r, c):
            def _f():
                nonlocal r, c
                if self.click(r, c):
                    self.player_status_won[self.current_player] = True
                    showinfo("You Won!", f"Player {FIELD_VALUES[self.current_player].capitalize()} has won!")
                    self.restart()

            return _f

        for i in range(3):
            for j in range(3):
                cmd = _click_command(i, j)
                b = tk.Button(frame, text=FIELD_VALUES[self.field[i][j]], font="20px", command=cmd)
                b.grid(row=i + row_offset, column=j, padx=5, pady=5, ipadx=5)
                self.buttons[i * 3 + j] = b
