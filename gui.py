import tkinter as tk
from tkinter import Misc, messagebox

from draw import Drawer
from field import Field, State
from misc import Timer


class App(tk.Frame):
    
    def __init__(self, master: Misc) -> None:
        super().__init__(master)
        # fill and resize
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        self.timer = Timer()
        self.gui = MainMenu(self)
        self.gui.grid()
    
    def start_game(self) -> None:
        self.gui.grid_forget()
        self.game = Field(10, 10, 10)
        self.drawer = Drawer(self, self.game, self.onOpen, self.onMark)
        self.drawer.grid()
    
    def onOpen(self, x: int, y: int) -> None:
        if self.game.state is State.New:
            self.timer.start()
        
        self.game.onOpen(x, y)
        self.drawer.update()
        
        match self.game.state:
            case State.New | State.Normal:
                pass
            case State.Win:
                self.timer.stop()
                self.win()
            case State.Lost:
                self.timer.stop()
                self.lost()
            case _:
                raise NotImplementedError("Unknown field state {}"
                                          .format(self.game.state))
    
    def onMark(self, x: int, y: int) -> None:
        self.game.onMark(x, y)
        self.drawer.update()
    
    def win(self):
        print("Win!")
        messagebox.showinfo("Congrac!", 
                            f"You won! Your time {self.timer.passed()}")
        self.game_over()
    
    def lost(self):
        print("Gameover!")
        messagebox.showinfo("Game Over!",  
                            f"You lost! Your time {self.timer.passed()}")
        self.game_over()
        
    def game_over(self) -> None:
        self.drawer.destroy()
        self.gui.grid()

class MainMenu(tk.Frame):
    
    def __init__(self, master: App) -> None:
        super().__init__(master)
        start = tk.Button(self, text="Новая игра", command=master.start_game)
        start.grid()

if __name__ == "__main__":
    root = tk.Tk()
    App(root).grid()
    root.mainloop()