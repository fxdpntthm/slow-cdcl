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
        self.decides = []           
        self.added = []

    def __str__(self):
        return self.data[-1].__str__()

    def __repr__(self):
        return self.__str__()

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
        self.added.append(lit)

    def decide(self) -> int:
        """
        Returns the first unassigned literal
        """

        i = 1
        while i <= self.size:
            if not (self.has(i) or self.has(-1*i)):
                break
            i += 1
        print(f"decide {i}")
        self.add_decide(i)

        return i


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
        # if self.out_of_range(lit):
        #     print(f"{lit} out of range of model {self.data[-1]}")
        #     return False

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

        #print(self.data, level, negating_literal)
        assert self.data[-1][negating_literal] == 1

        # flip the literal
        # TODO: 
        self.data[-1][negating_literal] = 0
        self.data[-1][-1 * negating_literal] = 1
        # print(f"Model after pop_n: {self.data}")

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
        while i <= cl.size:
            if  ((cl.data[i] == 1 and self.data[-1][i] == 1)
                or (cl.data[-1 * i] == 1 and self.data[-1][-1 * i] == 1)):
                return True
            i += 1
        # print(f"satisfies_clause False\n {self.data[-1]}\n {cl}")
        return False

    def makes_unit(self, cl: Clause) -> Optional[int]:
        """
        Returns whether a clause is a unit clause
        If it is a unit clause, returns the unit literal
        Assmumes clause is consistent
        i.e.   forall i clause.data[i] == 1 <==> clause.data[-i] = 0
           and forall i clause.data[-i] == 1 <==> clause.data[i] = 0
        """

        # falsifying = False
        unit_literal = None
        lit_count = 0
        i = 1
        while i <= self.size:
            while (cl.data[i] == 0 and cl.data[-1*i] == 0 and i <= self.size
                    and (self.has(i) or self.has(-1 * i))):
                i+=1



            if cl.data[i] == 1:
                lit_count+=1
                if self.has(i): # this clause is already satisfied so skip
                    return None
                else:
                    if unit_literal is None and not self.has(-1*i):
                        unit_literal = i
                        i += 1
                        continue
                    else: return None # the clause is unresolved

            if cl.data[-1*i] == 1:
                lit_count+=1
                if self.has(-1*i): # this clause is already satisfied so skip
                    return None
                else:
                    if unit_literal is None and not self.has(i):
                        unit_literal = -1*i
                        i += 1
                        continue
                    else:
                        return None
                    # else: return (False, None) # the clause is unresolved
            i += 1

        # at this point,  unresolved is non 0 value
        assert unit_literal is not None
        return unit_literal


    def falsifies_clause(self, cl: Clause) -> bool:
        """
        Returns true if the model falsifies the clause
        (ie. model has a negation for every literal in the clause)
        TODO: Find a bitwise operator to do this
        """
        i = 1
        count = 0
        while i <= cl.size:
            # while ((cl.data[i] == 0 or cl.data[-1 * i] == 0)
            #        and i <= cl.size): i += 1

            if ((cl.data[i] == 1 and self.has(-1 * i))
                  or (cl.data[-1 * i] == 1 and self.has(i))):
                count += 1

            # if (cl.data[i] == 1 and self.has(i)): return False # should never happen
            # if (cl.data[-1*i] == 1 and self.has(-1*i)): return False # should never happen
            i = i + 1


        # print(f"---\nmodel:\n{self.data[-1]}\nclause:\n{cl}\n---{count} {cl.literal_size}\n")
        # i has to be of size cl.size here
        return (count == cl.literal_size)




        """while i <= cl.size:

            if i == cl.size:
                return False

            if self.has(i) and cl.data[i] == 1:
                return False
            if self.has(-1*i) and cl.data[-1*i] == 1:
                return False
            if not (self.has(i) and self.has(-1*i)):
                unresolved = True
            i += 1

        print(f"falsifies_clause {not unresolved} \n {self.data[-1]}\n {cl}")
        return (not unresolved)
"""

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


    def check_clauses(self, unresolved_clauses: list[Clause]) -> (list[Clause],list[Clause]):
        unresolved, resolved = [], []
        for clause in unresolved_clauses:
            if self.satisfies_clause(clause):
                resolved.append(clause)
            else:
                unresolved.append(clause)

        return (unresolved, resolved)

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
