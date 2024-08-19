from itertools import product
from operator import mul
from random import sample, seed
from typing import Generator

import numpy as np

Pos = tuple[int, int]

class TooManyBombs(BaseException):
    """Too many bombs for this field size"""

class Cell:
    
    def __init__(self) -> None:
        self.open = False
        self.bomb = False
        self.near = 0
    
    def __repr__(self) -> str:
        if not self.open:
            return "#"
        if self.bomb:
            return "*"
        if self.near:
            return str(self.near)
        return "_"

class Field:
    
    def __init__(self, width: int, height: int) -> None:
        self.size = self.width, self.height = width, height
        self.field = np.array([[Cell() for _ in range(self.width)] 
                               for _ in range(self.height)])
    
    def neighs(self, x: int, y: int) -> Generator[Pos, None, None]:
        for o_y, o_x in product(range(-1, 2), repeat=2):
            if o_x == 0 == o_y:
                continue
            n_x, n_y = x+o_x, y+o_y
            if not 0 <= n_y < self.height:
                continue
            if not 0 <= n_x < self.width:
                continue
            yield n_y, n_x
    
    def put_bombs(self, n_bombs: int, safe_x: int, safe_y: int) -> None:
        if n_bombs >= mul(*self.size):
            raise TooManyBombs(f"{n_bombs = }, {self.size = }")
        cells_coords = list(product(range(self.width), range(self.height)))
        n = 0
        for x, y in sample(cells_coords, k=n_bombs+1):
            if n == n_bombs:
                break
            if (x, y) == (safe_x, safe_y):
                continue
            self.field[y, x].bomb = True
            for n_y, n_x in self.neighs(x, y):
                self.field[n_y, n_x].near += 1
            n += 1
    
    def open(self, x: int, y: int) -> bool:
        cell = self.field[y, x]
        if cell.open:
            return False
        if cell.bomb:
            return True
        cell.open = True
        if not cell.near:
            for n_y, n_x in self.neighs(x, y):
                self.open(n_x, n_y)
        return False
    
    def open_all(self):
        for cell in self.field.flatten():
            cell.open = True
    
    def __repr__(self) -> str:
        return str(self.field)
            
if __name__ == "__main__":
    seed(1)
    w, h = 3, 3
    field = Field(w, h)
    field.put_bombs(1, 0, 0)
    field.open(0, 0)
    
    print(field)
    
    print(field.field[0, 2].oleg())
    # field.open_all()


