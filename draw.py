import tkinter as tk
from tkinter import messagebox
from functools import partial

from field import Field


class Drawer:
    
    def __init__(self) -> None:
        self.new = True
        self.field = Field(10, 10)
        self.app = tk.Tk()
        
        self.buttons = list()
        for y in range(self.field.height):
            self.buttons.append(list())
            for x in range(self.field.width):
                button = tk.Button(self.app, width=2, height=1, text=" ",
                                   command=partial(self.onButtonClick, x, y))
                button.grid(column=x, row=y)
                self.buttons[-1].append(button)
        
        self.app.mainloop()

    def onButtonClick(self, x: int, y: int):
        if self.new:
            self.field.put_bombs(10, x, y)
            self.new = False
        if self.field.open(x, y):
            self.over()
        self.update()
        if not self.field.left:
            self.win()
    
    def update(self):
        for y in range(self.field.height):
            for x in range(self.field.width):
                self.buttons[y][x].config(text=str(self.field.field[y, x]))
                self.buttons[y][x].update_idletasks()
    
    def win(self):
        print("Win!")
        messagebox.showinfo("Congrac!",  "Congrac! You won!")
        self.app.quit()
    
    def over(self):
        print("Gameover!")
        messagebox.showinfo("Game Over!",  "Game Over!")
        self.app.quit()

if __name__ == "__main__":
    app = Drawer()