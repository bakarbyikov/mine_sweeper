import json
import tkinter as tk
from tkinter import Misc, StringVar, Variable, messagebox
from tkinter import ttk

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
        # messagebox.showinfo("Congrac!",
        #                     f"You won! Your time {}")
        name = AskName(self, self.timer.passed()).get_name()
        Leaderboaed(self).save(name, self.timer.passed())
        self.master.game_over()

    def lost(self):
        print("Gameover!")
        messagebox.showinfo("Game Over!",
                            f"You lost!")
        self.master.game_over()


class AskName(tk.Toplevel):
    def __init__(self, master: Misc, time):
        super().__init__(master)
        self.title("What is your name?")
        tk.Label(self, text=f"You won! Your time is {time}").grid()
        self.entry = tk.Entry(self)
        self.entry.grid()
        tk.Button(self, text="Ok", command=self.close).grid()

    def get_name(self):
        self.mainloop()
        return self.entry.get()

    def close(self):
        self.quit()


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
        self.gui = MainMenu(self)
        self.gui.grid()


class MainMenu(tk.Frame):

    def __init__(self, master: App) -> None:
        super().__init__(master)
        start = tk.Button(self, text="Новая игра", command=master.start_game)
        start.grid()

        oleg = Leaderboaed(self)
        oleg.load()
        oleg.grid()


class Leaderboaed(ttk.Treeview):

    def __init__(self, master: Misc) -> None:
        super().__init__(master, column=("name", "time"))
        self.column("#0", width=0, stretch=tk.NO)
        self.column("name", anchor=tk.CENTER, width=80)
        self.column("time", anchor=tk.CENTER, width=100)
        self.heading("name", text="name")
        self.heading("time", text="time")

    def load(self, path: str = "score.txt"):
        try:
            with open(path, "r+") as file:
                for i, row in enumerate(file.readlines()):
                    self.insert(parent='', index='end', iid=i,
                                text='', values=row.split())
        except FileNotFoundError:
            pass

    def save(self, name: str, time: str, path: str = "score.txt"):
        with open(path, "a+") as file:
            print(name, time, file=file)


if __name__ == "__main__":
    root = tk.Tk()
    App(root).grid()
    root.mainloop()
