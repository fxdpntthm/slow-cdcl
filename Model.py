from typing import *
import numpy as np
from Clause import Clause

class Model:
    """
    Model class that holds literal assignments in levels, implemented as list of numpy arrays
    """
    def __init__(self, literals: int):
        self.data = [np.zeros(2 * literals + 1, dtype="int8")]
        self.size = literals
        self.decides = []     # keeping this because its required for DPLL backtrack

    def consistent(self, lit: int) -> bool:
        """
        Returns false if a negation of a literal (that is to be added) is true
        """
        return self.data[-1][-1 * lit] == 0

    def out_of_range(self, lit: int) -> bool:
        """
        Returns false if literal is out of range (not of the array, but the list of literals)
        """
        return abs(lit) == 0 or abs(lit) > (len(self.data[-1]) - 1)/2

    def add(self, lit: int):
        """
        Adds a literal to the latest level of the model
        """

        if not self.consistent(lit):
            print(f"Adding {lit} to {self.data[-1]} will make it inconsistent")

        if self.out_of_range(lit):
            print(f"{lit} out of range of model {self.data[-1]}")
            return

        self.data[-1][lit] = 1

    def add_decide(self, lit: int):
        """
        Copies the latest level, and adds the literal to the level
        """
        self.data.append(np.copy(self.data[-1]))
        self.decides.append(lit)

        self.add(lit)


    def get_data(self) -> np.ndarray:
        return self.data

    def contains_clause(self, cl: Clause) -> bool:
        """
        Returns true if the clause is a subset of the model
        (ie. every literal in the clause is satisfied by the model).
        This is implemented by using (clause OR model) == model (where OR is element-wise OR),
        which is equivalent to the subset operation
        """
        return np.array_equal((cl.data | self.data[-1]).astype("int8"), self.data[-1])

    def has(self, lit: int) -> bool:
        """
        Returns true if literal is satisfied by the model
        """
        if self.out_of_range(lit):
            print(f"{lit} out of range of model {self.data[-1]}")
            return False

        return self.data[-1][lit] == 1


    def pop_decide(self) -> int:
        """
        Pops the latest level in the model,
        and returns the literal that was decided
        at that level
        TODO: nth level pop
        """
        if not self.has_decide():
            return 0

        decision = self.decides.pop()
        self.data.pop()
        return decision

    def pop_n(self, level: int, negating_literal: int):

        self.data = self.data[:level + 1]
        self.decides = self.decides[:level + 1]

        if len(self.data) == 0:
            self.data = [np.zeros(2 * self.size + 1, dtype="int8")]

        print(self.data, level, negating_literal)
        assert self.data[-1][negating_literal] == 1

        # flip the literal
        self.data[-1][negating_literal] = 0
        self.data[-1][-1 * negating_literal] = 1
        print(f"Model after pop_n: {self.data}")

    def has_decide(self) -> bool:
        """
        Returns true if there is something has been decided on in the model
        """
        return len(self.decides) > 0

    def satisfies_clause(self, cl: Clause) -> bool:
        """
        Returns true if the model satisfies the clause
        (ie. if there is a literal that is in the clause and the model)
        """
        i = 1
        while i <= self.size:
            if  ((cl.data[i] == 1 and self.data[-1][i] == 1)
                or (cl.data[-1 * i] == 1 and self.data[-1][-1 * i] == 1)):
                return True
            i += 1

        return False

    def makes_unit(self, cl: Clause) -> (bool, Optional[int]):
        """
        Returns whether a clause is a unit clause
        If it is a unit clause, returns the unit literal
        Assmumes clause is consistent
        i.e. forall i clause.data[i] and clause.data[-i] are never set to one at the same time
        """

        # falsifying = False
        unresolved = None

        # obvious shortcut case
        if cl.size == 1:
            return (True, cl.data[1])

        i = 1
        while i <= self.size:
            while cl.data[i] == 0 and cl.data[-1*i] == 0 and i <= self.size:
                i+=1

            if cl.data[i] == 1:
                if self.has(i): # this clause is already satisfied so skip
                    return (False, None)
                else:
                    if unresolved == 0: unresolved = i
                    else: return (False, None) # the clause is unresolved

            if cl.data[-1*i] == 1:
                if self.has(-1*i): # this clause is already satisfied so skip
                    return (False, None)
                else:
                    if unresolved == 0: unresolved = i
                    else: return (False, None) # the clause is unresolved
            i += 1

        # at this point,  unresolved is non 0 value
        assert unresolved != 0
        return (True,unresolved)


    def falsifies_clause(self, cl: Clause) -> bool:
        """
        Returns true if the model falsifies the clause
        (ie. model has a negation for every literal in the clause)
        TODO: Find a bitwise operator to do this
        """
        i = 1
        while i <= self.size:
            if (not self.has(i)) and (not self.has(-1*i)):
                return False

            if cl.data[i] == 1 and self.has(i):
                return False

            if cl.data[-1*i] == 1 and self.has(-1*i):
                return False

            i += 1

        return True

    def compute_backjump_level(self, cl: Clause) -> (int,int):
        """
        For a given model, computes the level for backjump
        """
        i = 0
        while i < len(self.data):
            for j in cl.to_list():
                if self.data[i][j] == 1:
                    return (i,j)
            i += 1



    def print(self):
        return str(self.data)

    def to_list(self) -> list[int]:
        """
        Returns the model as a list of literals ([1,2,-3...])
        could be replaced by an iterator later...
        """
        cl = []
        i = 1
        while i <= self.size:
            if self.data[-1][i] == 1:
                cl.append(i)
            if self.data[-1][-1*i] == 1:
                cl.append(-1*i)

            i += 1

        return cl
