from typing import *
import numpy as np

class Clause:
    """
    Clause class that holds literals implemented as a numpy array
    """
    def __init__(self, literals: int):

        self.data = np.zeros(2 * literals + 1, dtype="int8")
        self.size = literals
        self.literal_size = 0

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.__str__()

    def consistent(self, lit: int) -> bool:
        """
        Returns false if a negation of a literal (that is to be added) is true
        """
        return self.data[-1 * lit] == 0

    def out_of_range(self, lit: int) -> bool:
        """
        Returns false if literal is out of range (not of the array, but the list of literals)
        """
        return abs(lit) == 0 or abs(lit) > (len(self.data) - 1)/2

    def add(self, lit: int):
        """
        Adds a literal to the clause
        """
        assert not self.out_of_range(lit), f"literal out of range: {lit}, clause: {self.data}"

        if not self.consistent(lit):
            print(f"Clause has both literal and its negation: {self.data}")

        self.data[lit] = 1
        self.literal_size += 1

    def remove(self, lit: int):
        """
        Removes a literal from a clause
        """
        if self.data[lit] == 0:
            print(f"Literal already not in clause: {lit} Clause: {self.data}")

        self.data[lit] = 0


    def has(self,lit: int) -> bool:
        """
        Returns true if the clause has a literal
        """
        if self.out_of_range(lit):
            print(f"literal out of range: {lit}, size: {self.data}")
            return

        return self.data[lit] == 1

    def negated(self):
        """
        Returns a negated clause object (ie. every literal in the clause is negated)
        """
        negated = Clause(self.size)
        negated.data = np.copy(self.data)

        i = 1
        while i <= self.size:
            negated.data[i], negated.data[-1*i] = negated.data[-1*i], negated.data[i]
            i += 1

        return negated

    def negated_minus_one(self, lit: int):
        """
        Used in unit propagation
        """
        negated = self.negated()
        negated.remove(-1 * lit)
        return negated

    def to_list(self) -> list[int]:
        """
        just returns the clause as a list of literals ([1,2,-3...])
        could be replaced by an iterator later...
        """
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
