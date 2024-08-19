import tkinter as tk
from functools import partial
from tkinter import messagebox

from field import CellType, Field


class Drawer:
    
    def __init__(self) -> None:
        self.new = True
        self.field = Field(10, 10)
        font = ("Terminal", 20, "bold")
        self.app = tk.Tk()
        
        self.buttons = list()
        for y in range(self.field.height):
            self.buttons.append(list())
            for x in range(self.field.width):
                button = tk.Button(self.app, text=" ", font=font,
                                   command=partial(self.onButtonClick, x, y))
                button.grid(column=x, row=y)
                button.bind("<Button-3>", partial(self.mark, x, y))
                self.buttons[-1].append(button)
        
        self.app.mainloop()
    
    def mark(self, x: int, y: int, *_):
        self.field.mark(x, y)
        self.update()

    def onButtonClick(self, x: int, y: int):
        if self.new:
            self.field.put_bombs(10, x, y)
            self.new = False
        if self.field.open(x, y):
            self.over()
        self.update()
        if not self.field.left:
            self.field.open_all()
            self.update()
            self.win()
    
    def update(self):
        for y in range(self.field.height):
            for x in range(self.field.width):
                self.update_button(x, y, self.field.field[y, x].type())
    
    def update_button(self, x: int, y: int, cell: CellType) -> None:
        button = self.buttons[y][x]
        match cell:
            case CellType.Bomd | CellType.Marked:
                bg = "red"
            case _:
                bg = "SystemButtonFace"
        button.config(text=cell.value, bg=bg)
        button.update_idletasks()
    
    def win(self):
        print("Win!")
        messagebox.showinfo("Congrac!",  "Congrac! You won!")
        self.app.quit()
    
    def over(self):
        print("Gameover!")
        messagebox.showinfo("Game Over!",  "You lost!")
        self.app.quit()

if __name__ == "__main__":
    app = Drawer()