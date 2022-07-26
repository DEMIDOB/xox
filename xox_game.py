import tkinter as tk
from functools import partial

import numpy as np

FIELD_VALUES = ["x", "o", " "]


class XoxTriedToChangeAlreadyOccupiedCellError(Exception):
    pass


class XoxGame:
    def __init__(self):
        self.field = np.zeros((3, 3), dtype=int)
        self.buttons: [tk.Button] = [None for _ in range(9)]
        self.field -= 1

        self.players = ["x", "o"]
        self.current_player = 0

        self.active = True

    def click(self, r, c):
        assert r in range(3) and c in range(3), f"Wrong grid indexing ({r}, {c})"
        assert self.active, "Attempt to play an inactive game"

        if not self.field[r][c] == -1:
            raise XoxTriedToChangeAlreadyOccupiedCellError()

        self.field[r][c] = self.current_player
        self.buttons[r * 3 + c]["text"] = FIELD_VALUES[self.current_player]
        self.current_player = int(not self.current_player)

    def draw(self, frame: tk.Frame, row_offset=0):
        for i in range(3):
            for j in range(3):
                cmd = partial(self.click, i, j)
                b = tk.Button(frame, text=FIELD_VALUES[self.field[i][j]], font="20px", command=cmd)
                b.grid(row=i + row_offset, column=j, padx=5, pady=5, ipadx=5)
                self.buttons[i * 3 + j] = b
