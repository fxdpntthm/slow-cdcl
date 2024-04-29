from typing import *
import numpy as np

class Clause:
    def __init__(self, literals: int):
        self.data = np.zeros(2 * literals + 1, dtype="int8")
        self.size = literals

    def consistent(self, lit: int) -> bool:
        return self.data[-1 * lit] == 0
    
    def out_of_range(self, lit: int) -> bool:
        return abs(lit) == 0 or abs(lit) > (len(self.data) - 1)/2

    def add(self, lit: int):
        if self.out_of_range(lit):
            print(f"literal out of range: {lit}, clause: {self.data}")
            return

        if not self.consistent(lit):
            print(f"Clause has both literal and its negation: {self.data}")

        self.data[lit] = 1

    def remove(self, lit: int):
        if self.data[lit] == 0:
            print(f"Literal already not in clause: {lit} Clause: {self.data}")

        self.data[lit] = 0
        
            
    def has(self,lit: int) -> bool:
        if self.out_of_range(lit):
            print(f"literal out of range: {lit}, size: {self.data}")
            return
        
        return self.data[lit] == 1

    def negated(self):
        negated = Clause(self.size)
        for i in self.to_list():
            negated.add(-1 * i)
        
        return negated

    def negated_minus_one(self, lit: int):
        """
        Used in unit propagation
        """
        negated = self.negated()
        negated.remove(-1 * lit)
        return negated
    
    def to_list(self) -> list[int]:
        # just returns the clause as a list of literals ([1,2,-3...])
        # could be replaced by an iterator later...

        cl = []
        i = 1
        while i <= self.size:
            if self.data[i] == 1:
                cl.append(i)
            i += 1
        
        i = -1
        while i >= -1 * self.size:
            if self.data[i] == 1:
                cl.append(i)
            i -= 1

        return cl
