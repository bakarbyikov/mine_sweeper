import tkinter as tk
from tkinter import Misc, StringVar, Variable, messagebox

from draw import Drawer
from field import Field, State
from misc import Timer

class TimerLabel(tk.Frame):
    def __init__(self, master: Misc, timer: Timer) -> None:
        super().__init__(master)
        self.timer = timer
        self.text_variable = StringVar()
        self.update()
        tk.Label(self, textvariable=self.text_variable).grid()
    
    def update(self) -> None:
        self.text_variable.set(f"Время: {self.timer.passed_whole()}")
        self.after(1000, self.update)

class Game(tk.Frame):
    
    def __init__(self, master: Misc, field_args: dict[str, int]) -> None:
        super().__init__(master)
        
        self.timer = Timer()
        TimerLabel(self, self.timer).grid()
        self.field = Field(**field_args)
        self.drawer = Drawer(self, self.field, self.onOpen, self.onMark)
        self.drawer.grid()
    
    def onOpen(self, x: int, y: int) -> None:
        if self.field.state is State.New:
            self.timer.start()
        
        self.field.onOpen(x, y)
        self.drawer.update()
        
        match self.field.state:
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
                                          .format(self.field.state))
    
    def onMark(self, x: int, y: int) -> None:
        self.field.onMark(x, y)
        self.drawer.update()
    
    def win(self):
        print("Win!")
        messagebox.showinfo("Congrac!", 
                            f"You won! Your time {self.timer.passed()}")
        self.master.game_over()
    
    def lost(self):
        print("Gameover!")
        messagebox.showinfo("Game Over!",  
                            f"You lost! Your time {self.timer.passed()}")
        self.master.game_over()

class App(tk.Frame):
    
    def __init__(self, master: Misc) -> None:
        super().__init__(master)
        # fill and resize
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        self.gui = MainMenu(self)
        self.gui.grid()
    
    def start_game(self) -> None:
        self.gui.grid_forget()
        self.game = Game(self, {'width': 10, 'height': 10, 'n_bombs': 10})
        self.game.grid()
    
    def game_over(self) -> None:
        self.game.destroy()
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