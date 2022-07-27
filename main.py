import tkinter as tk
from tkinter.messagebox import showerror

from xox_game import *


def main():
    game = XoxGame()

    root = tk.Tk()
    root.title("XOX")
    
    frame = tk.Frame(root, padx=20, pady=10)

    tk.Label(frame, text="XOX").grid(row=0, column=0, columnspan=3)
    game.draw(frame, row_offset=1)

    frame.pack(expand=True)
    root.eval('tk::PlaceWindow . center')

    def report_callback_exception(self, exc: Exception, val, tb):
        showerror("Error", message=str(exc))
        if isinstance(exc, ShouldRestartTheGame):
            nonlocal game
            game.restart()
        raise exc

    tk.Tk.report_callback_exception = report_callback_exception
    root.mainloop()


if __name__ == '__main__':
    main()
