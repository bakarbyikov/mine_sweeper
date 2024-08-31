import tkinter as tk
from tkinter import Misc

from field import CellType, Field


def wrapper(f, x, y, *_):
    def inner(*_):
        return f(x, y)
    return inner

class Drawer(tk.Frame):
    
    def __init__(self, master: Misc, field: Field, onOpen, onMark) -> None:
        super().__init__(master)
        self.field = field
        font = ("Terminal", 20, "bold")
        
        self.buttons = list()
        for y in range(self.field.height):
            self.buttons.append(list())
            for x in range(self.field.width):
                button = tk.Button(self, font=font,
                                   command=wrapper(onOpen, x, y))
                button.grid(column=x, row=y)
                button.bind("<Button-3>", wrapper(onMark, x, y))
                self.buttons[-1].append(button)
        self.update()
    
    def update(self):
        for y in range(self.field.height):
            for x in range(self.field.width):
                self.update_button(x, y, self.field.field[y, x].type())
        self.update_idletasks()
    
    def update_button(self, x: int, y: int, cell: CellType) -> None:
        button = self.buttons[y][x]
        match cell:
            case CellType.Bomd | CellType.Marked:
                bg = "red"
            case CellType.Hidden:
                bg = "gray"
            case _:
                bg = "SystemButtonFace"
        button.config(text=cell.value, bg=bg)

if __name__ == "__main__":
    game = Field(10, 10, 10)
    root = tk.Tk()
    
    def onOpen(*args):
        game.onOpen(*args)
        drawer.update()
    def onMark(*args):
        game.onMark(*args)
        drawer.update()
    
    drawer = Drawer(root, game, onOpen, onMark)
    drawer.grid()
    root.mainloop()