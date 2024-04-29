from typing import *
import numpy as np
from Clause import Clause

class Model:
    """ 
    Model class that holds literal assignments in levels
    """
    def __init__(self, literals: int):
        self.data = [np.zeros(2 * literals + 1, dtype="int8")]
        self.size = literals
        self.decides = []     # keeping this because its required for DPLL backtrack
        
    def consistent(self, lit: int) -> bool:
        return self.data[-1][-1 * lit] == 0
    
    def out_of_range(self, lit: int) -> bool:
        return abs(lit) == 0 or abs(lit) > (len(self.data[-1]) - 1)/2

    def add(self, lit: int):
        if not self.consistent(lit):
            print(f"Adding {lit} to {self.data[-1]} will make it inconsistent")
        
        if self.out_of_range(lit):
            print(f"{lit} out of range of model {self.data[-1]}")
            return

        self.data[-1][lit] = 1
    
    def add_decide(self, lit: int):
        self.data.append(np.copy(self.data[-1])) 
        self.decides.append(lit)
        
        self.add(lit)

        
    def get_data(self) -> np.ndarray:
        return self.data
    
    def contains_clause(self, cl: Clause) -> bool:
        return np.array_equal((cl.data | self.data[-1]).astype("int8"), self.data[-1])

    def has(self, lit: int) -> bool:
        if self.out_of_range(lit):
            print(f"{lit} out of range of model {self.data[-1]}")
            return False
        
        return self.data[-1][lit] == 1

    
    def pop_decide(self) -> int:
        if not self.has_decide():
            return 0

        decision = self.decides.pop()
        self.data.pop()
        return decision

    def has_decide(self) -> bool:
        return len(self.decides) > 0

    def print(self):
        return str(self.data)

    def to_list(self) -> list[int]:
        # just returns the model as a list of literals ([1,2,-3...])
        # could be replaced by an iterator later...

        cl = []
        i = 1
        while i <= self.size:
            if self.data[-1][i] == 1:
                cl.append(i)
            i += 1
        
        i = -1
        while i >= -1 * self.size:
            if self.data[-1][i] == 1:
                cl.append(i)
            i -= 1

        return cl
