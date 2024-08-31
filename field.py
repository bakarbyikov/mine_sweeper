from enum import Enum, auto
from itertools import product
from operator import mul
from random import sample, seed
from typing import Generator

import numpy as np

Pos = tuple[int, int]

class TooManyBombs(BaseException):
    """Too many bombs for this field size"""

class CellType(Enum):
    Marked = "!"
    Empty = " "
    Hidden = "#"
    Bomd = "*"
    Digit1 = "1"
    Digit2 = "2"
    Digit3 = "3"
    Digit4 = "4"
    Digit5 = "5"
    Digit6 = "6"
    Digit7 = "7"
    Digit8 = "8"

class State(Enum):
    New = auto()
    Win = auto()
    Lost = auto()
    Normal = auto()

class Cell:
    
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self.marked = False
        self.open = False
        self.bomb = False
        self.near = 0
    
    def type(self) -> CellType:
        if self.marked:
            return CellType.Marked
        if not self.open:
            return CellType.Hidden
        if self.bomb:
            return CellType.Bomd
        if self.near:
            return CellType(str(self.near))
        return CellType.Empty
    
    def __repr__(self) -> str:
        return self.type().value

class Field:
    
    def __init__(self, width: int, height: int, n_bombs: int) -> None:
        self.size = self.width, self.height = width, height
        self.field = np.array([[Cell() for _ in range(self.width)] 
                               for _ in range(self.height)])
        self.state = State.New
        self.n_bombs = n_bombs
        self.left = None
    
    def neighs(self, x: int, y: int) -> Generator[Pos, None, None]:
        for o_y, o_x in product(range(-1, 2), repeat=2):
            if o_x == 0 == o_y:
                continue
            n_x, n_y = x+o_x, y+o_y
            if not 0 <= n_y < self.height:
                continue
            if not 0 <= n_x < self.width:
                continue
            yield n_x, n_y
    
    def reset(self) -> None:
        self.__init__(self.width, self.height, self.n_bombs)
        # list(map(Cell.reset, self.field.flatten()))
    
    def put_bombs(self, safe_x: int, safe_y: int) -> None:
        if self.n_bombs >= mul(*self.size):
            raise TooManyBombs(f"{self.n_bombs = }, {self.size = }")
        self.left = mul(*self.size) - self.n_bombs
        cells_coords = list(product(range(self.width), range(self.height)))
        n = 0
        for x, y in sample(cells_coords, k=self.n_bombs+1):
            if n == self.n_bombs:
                break
            if (x, y) == (safe_x, safe_y):
                continue
            self.field[y, x].bomb = True
            for n_x, n_y in self.neighs(x, y):
                self.field[n_y, n_x].near += 1
            n += 1
    
    def count_closed(self, x: int, y: int) -> int:
        number = 0
        for n_x, n_y in self.neighs(x, y):
            number += not self.field[n_y, n_x].open
        return number
    
    def count_marked(self, x: int, y: int) -> int:
        number = 0
        for n_x, n_y in self.neighs(x, y):
            number += self.field[n_y, n_x].marked
        return number
    
    def mark_around(self, x: int, y: int) -> None:
        cell = self.field[y, x]
        n_closed = self.count_closed(x, y)
        if n_closed != cell.near:
            return
        on_off = n_closed != self.count_marked(x, y)
        for nx, ny in self.neighs(x, y):
            neigh = self.field[ny, nx]
            if neigh.open:
                continue
            neigh.marked = on_off
    
    def mark(self, x: int, y: int) -> None:
        cell = self.field[y, x]
        if cell.open:
            self.mark_around(x, y)
            return
        cell.marked = not cell.marked
    
    def onOpen(self, x: int, y: int) -> None:
        if (self.state is State.Win
            or self.state is State.Lost):
            self.reset()
            self.state = State.New
            return
        if self.state is State.New:
            self.put_bombs(x, y)
            self.state = State.Normal
        if self.open(x, y):
            self.state = State.Lost
            self.open_all()
            return
        if not self.left:
            self.state = State.Win
            self.open_all()
    
    def open_around(self, x: int, y: int) -> bool:
        cell = self.field[y, x]
        if self.count_marked(x, y) != cell.near:
            return
        blown = False
        for nx, ny in self.neighs(x, y):
            blown |= self.open(nx, ny, around=False)
        return blown
    
    def open(self, x: int, y: int, around=True) -> bool:
        cell = self.field[y, x]
        if cell.open:
            if around:
                return self.open_around(x, y)
            return False
        if cell.marked:
            return False
        if cell.bomb:
            return True
        cell.open = True
        self.left -= 1
        if not cell.near:
            for n_x, n_y in self.neighs(x, y):
                self.open(n_x, n_y)
        return False
    
    def open_all(self):
        for cell in self.field.flatten():
            cell.open = True
    
    def __repr__(self) -> str:
        return str(self.field)
