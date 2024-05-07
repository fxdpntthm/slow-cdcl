from typing import *

from Clause import Clause
from bitarray import bitarray

class Model:
    """
    Model class that holds literal assignments in levels, implemented as list of numpy arrays
    """
    def __init__(self, literals: int):
        self.data = [bitarray([0] * (2 * literals + 1))]
        self.size = literals
        self.literal_lvls = {}
        self.lit_lvl = 0

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
            print(f"Adding {lit} to {self.to_list()} will make it inconsistent")

        if self.out_of_range(lit):
            print(f"{lit} out of range of model {self.data[-1]}")
            return

        self.data[-1][lit] = 1
        self.lit_lvl = self.lit_lvl + 1
        self.literal_lvls[lit] = self.lit_lvl

    def decide(self) -> int:
        """
        Returns the first unassigned literal
        """

        i = 1
        while i < self.size:
            if not (self.has(i) or self.has(-1*i)):
                break
            i += 1
        #print(f"decide {i}")
        self.add_decide(i)

        return i

    def is_complete(self) -> bool:
        i = 1
        while i <= self.size:
            if not (self.has(i) or self.has(-1*i)):
                return False
            i += 1
        return True

    def add_decide(self, lit: int):
        """
        Copies the latest level, and adds the literal to the level
        """
        self.data.append(self.data[-1].copy())

        self.add(lit)


    def get_data(self) -> bitarray:
        return self.data

    def contains_clause(self, cl: Clause) -> bool:
        """
        Returns true if the clause is a subset of the model
        (ie. every literal in the clause is satisfied by the model).
        This is implemented by using (clause OR model) == model (where OR is element-wise OR),
        which is equivalent to the subset operation
        """
        return (bitarray(cl.data) | self.data[-1]) == self.data[-1]

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
        """
        if not self.has_decide():
            return 0

        self.data.pop()
        return decision

    def pop_n(self, level: int, negating_literal: int):

        self.data = self.data[:level + 1]

        if len(self.data) == 0:
            self.data = [bitarray([0] * (2 * self.size + 1))]

        #print(self.data, level, negating_literal)
        assert self.data[-1][negating_literal] == 1

        # flip the literal
        self.data[-1][negating_literal] = 0
        self.data[-1][-1 * negating_literal] = 1
        # print(f"Model after pop_n: {self.data}")

    def has_decide(self) -> bool:
        """
        Returns true if there is something has been decided on in the model
        """
        return len(self.data) > 1

    def satisfies_clause(self, cl: Clause) -> bool:
        """
        Returns true if the model satisfies the clause
        (ie. if there is a literal that is in the clause and the model)
        """
        
        # run bitwise model AND clause and see if there are any 1's in the result 
        # (ie. at least 1 thing that is both in the model and the clause)
        return (self.data[-1] & cl.data).any()
        
       
    def makes_unit(self, cl: Clause) -> Optional[int]:
        """
        Returns whether a clause is a unit clause
        If it is a unit clause, returns the unit literal
        Assmumes clause is consistent
        i.e.   forall i clause.data[i] == 1 <==> clause.data[-i] = 0
           and forall i clause.data[-i] == 1 <==> clause.data[i] = 0
        """
        
        unit_literal = None

        i = 1
        while i <= self.size:
            while cl.data[i] == 0 and cl.data[-1*i] == 0 and i <= self.size:
                i += 1
            
            if i > self.size:
                return unit_literal
            
            if cl.data[i] == 1:
                if self.has(i):
                    #print(f"has {i} {cl.to_list()}")
                    return None
                
                if (not self.has(i)) and (not self.has(-1*i)):
                    if unit_literal:
                        return None
                    else:
                        unit_literal = i
            
                

            else:
                if self.has(-1*i):
                    #print(f"has {-1*i} {cl.to_list()}")
                    return None
                
                if (not self.has(i)) and (not self.has(-1*i)):
                    if unit_literal:
                        return None
                    else:
                        unit_literal = -1*i
            
            i += 1
                
        
        return unit_literal

             
        """unresolved_literals = list(filter(lambda x: not self.has(-1*x), cl.to_list()))
        if len(unresolved_literals) == 1:
            #print(f"Propogating... {unresolved_literals[0]}")
            return unresolved_literals[0]

        return None"""


    def falsifies_clause(self, cl: Clause) -> bool:
        """
        Returns true if the model falsifies the clause
        (ie. model has a negation for every literal in the clause)
        """

        negated = cl.negated()

        # do a model AND negated clause and return True if the no of 1's 
        # (ie. no of literals that are also in the model) 
        # is the same as the no of literals in the model
        return (negated.data | self.data[-1]) == self.data[-1]


    def compute_level(self, literal:int) -> int:
        """
        computes the level of the literal that is set
        """
        i = 0
        while i < len(self.data):
            if self.data[i][literal] == 0:
                i += 1
            else: return i




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


    def check_clauses(self, unresolved_clauses: list[Clause]) -> (list[Clause],list[Clause], Optional[Clause]):
        unresolved, resolved = [], []
        conflict_clause = None
        i = 0
        for clause in unresolved_clauses:
            if self.satisfies_clause(clause):
                resolved.append(clause)
            elif self.falsifies_clause(clause):
                conflict_clause = clause
                unresolved.append(clause)
            else:
                unresolved.append(clause)
            i += 1

        return (unresolved, resolved, conflict_clause)

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
