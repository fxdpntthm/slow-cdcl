import sys

from Model import Model
from Clause import Clause
from typing import *
import numpy as np

"""
The main file that gives an assignment to a Propositional Boolean Logic formula in a CNF format
or returns UNSAT
"""

def solve (clause_set: list[Clause], literals: int) -> Optional[Clause]:
    """
    The solver takes a formula or the clause_set
    of a list of lists. The inner list are the set of literals.

    the clause set [[1,-2,3], [2,3], [2], [-1, 2]]
    represents the formula
    [(A \/ -B \/ C) /\  (B \/ C) /\  B /\ (-A \/ B)]

    Currently working off of slide 30 in https://homepage.divms.uiowa.edu/~tinelli/classes/4980/Spring24/notes/06-dpll-cdcl.pdf

    Returns a satisfying list of assignments if there exists one
    If the clause set is unsatisfiable, return [0]
    """

    model = Model(literals)
    conflict_clause = None

    #print(f"Clauses: {clauses}")
    return solve_helper((clause_set,[]), model)



                              #unresolved   #satisfied
def solve_helper(clause_set: (list[Clause], list[Clause]), model: Model) -> Optional[Clause]:
    """
    The solver runs in the following manner:
    1. Checks if we have have unresolved clauses (If no, we have a satisfying model)
    2. Unit propagates clauses which we can (go to step 1)
    -- No unit propagation possible and we still have unresolved clauses then do step 3
    3. Decide on a literal (go to step)
    4.
    """


    (unresolved_clauses, satisfied_clauses) = clause_set
    conflict_clause = None


    # TODO: once restart is done, use restart instead of while true
    while len(unresolved_clauses) > 0:
        # print(f"Model:\n{model}\nUnresolved:\n{unresolved_clauses}")

        # run unit propagation as much as possible
        (unresolved_clauses, new_unit_clauses) = propagate_possible(unresolved_clauses, model)
        # print(f"After propagation: {still_unresolved_clauses}, {new_unit_clauses}")
        print("Propogating...")
        satisfied_clauses.extend(new_unit_clauses)

        if len(new_unit_clauses) > 0:
            # it is possible that this propagate makes other unresolved clauses unit
            continue

        # run decide as no propogation possible
        model.decide()

        unresolved, resolved = model.check_clauses(unresolved_clauses)

        unresolved_clauses = unresolved
        satisfied_clauses.extend(resolved)

        # get a failing clause, if any
        conflicting_clause = check_falsify(unresolved_clauses,model)

        if conflicting_clause: print(f"Model:\n{model}\nConflicting Clause:\n{conflicting_clause}")
        # if there's a failing clause and there are no decides left to reverse in the model
        # return UNSAT
        if conflicting_clause and (not model.has_decide()):
            print(f"Model:\n{model}\nConflicting Clause:\n{conflicting_clause}")
            return None


        # if there is a failing clause and there is a guess that can be backtracked on,
        # run backtrack. currently just dpll backtrack,
        # but conflict/explain/learn/backjump here in CDCL
        if conflicting_clause:
            print(f"Conflicting clause:\n{conflicting_clause}\nModel:\n{model}")
            conflict_clause = conflicting_clause
            conflict_clause = explain(unresolved_clauses + satisfied_clauses, model, conflict_clause)
            
            for clause in unresolved_clauses + satisfied_clauses:
                if np.array_equal(conflict_clause.data,clause.data):
                    # we have learned this clause already, so we have to have unsat at this point
                    print(f"trying to add a learned clause again {conflict_clause}")
                    return None

            new_clause_set = learn_backjump(unresolved_clauses + satisfied_clauses, model, conflict_clause)

            unresolved_clauses, satisfied_clauses = model.check_clauses(new_clause_set)

            #print(f"Model before learn: {model.data}")


    # We have a model which satisfies all the clauses
    return model.to_list()

"""
1 |-> x + y <= 0
2 |-> 4*x + z <= 1
"""


"""
RULES
Are we implementing RESTART?
"""



def sat(clause_set : list[Clause], model: Model) -> bool:
    """
    Returns true if all clauses in a clause set are satisfied by the current model
    """

    for clause in clause_set:
        if not model.satisfies_clause(clause):
            return False

    return True

def check_falsify(clause_set: list[Clause], model: Model) -> Optional[Clause]:
    """
    Returns the first clause in a clause set where
    the model has a negated assignment for every literal in that clause set
    If none exist, returns None
    """
    for clause in clause_set:
        if model.falsifies_clause(clause):
            return clause

    return None


def propagate_possible(unresolved_clauses: list[Clause], model: Model) -> (list[Clause], list[Clause]):
    """
    Finds a unit literal and splits unresolved_clauses into resolved and unresolved clauses
    The model parameter is modified by the function
    """

    (unresolved, resolved) = ([], [])
    #print(f"unresolved clauses {unresolved_clauses}")
    literal = None
    for clause in unresolved_clauses:
        literal = model.makes_unit(clause)

        if literal:
            #print(f"makes unit: {literal}")
            break


    if literal:
        model.add(literal)
        #print(f"Propagated\n{model}")
        return model.check_clauses(unresolved_clauses)
    else:
        return (unresolved_clauses,[])


def explain(clause_set: list[Clause], model: Model, conflict_clause: Clause) -> Clause:
    """
    Modifies the conflict clause
    """

    i = len(model.added) - 1

    while i >= 0:
        if model.has(model.added[i]) and conflict_clause.has(-1 * model.added[i]):
            clauses_with_l = filter(lambda x: x.has(model.added[i]), clause_set)
            for clause in clauses_with_l:
                copy = Clause(clause.size)
                copy.data = np.copy(clause.data)
                copy.remove(model.added[i])
                if model.satisfies_clause(copy):
                    conflict_clause.remove(-1*model.added[i]) 
                    for lit in copy.negated().to_list():
                        conflict_clause.add(lit)
                        return conflict_clause
        
        i -= 1
    

    """for literal in rev:
        if model.has(-1 * literal):
            clauses_with_lit = filter(lambda x: x.has(-1*literal), clause_set)
            c = []
            for clause in clauses_with_lit:
                copy = Clause(clause.size)
                copy.data = np.copy(clause.data)
                copy.remove(-1 * literal)
                copy = copy.negated()
                if model.satisfies_clause(copy):
                    c.append(copy)

            res = max(c, key=lambda x:)"""

        
                

    return clause

def learn_backjump(clause_set: list[Clause], model: Model, conflict_clause: Clause):
    """
    adds clauses from the conflict_clause to the clause_set
    """
    m2 = 0
    m2_lit = None
    max = 0
    max_literal = None
    for literal in conflict_clause.to_list():
        i = 0
        # finding the first level where negation of the literal was set
        while i < len(model.data):
            if model.data[i][-1 * literal] == 0:
                i += 1
                continue
            else:
                # we want to find the literal that was first set at the highest level
                if max < i:
                    m2 = max
                    m2_lit = max_literal
                    max = i
                    max_literal = -1 * literal
                elif m2 < i:
                    m2 = i
                    m2_lit = -1 * literal

            i += 1

    latest_level = model.data[-1]
    flip = self.decides[m2]
    model.data = model.data[:m2]
    

    model.data[-1][-1*flip] = 1

    """unresolved_clauses.append(learn_clause)
    print(f"learned clause {learn_clause}")
    #print(f"Clause set: {list(map(lambda x: x.to_list(), clause_set))}")
    (backjump_level, negating_literal) = model.compute_backjump_level(learn_clause)
    print(f"backjump_level: {backjump_level}, negating_literal {negating_literal}")
    model.pop_n(backjump_level,negating_literal)
    conflict_clause = None
    unresolved_clauses.extend(satisfied_clauses)
    satisfied_clauses = [] # forget all the satisfying clauses"""
    return clause_set + [conflict_clause]


"""
clause = [0, 1,2,.... -2,-1]
"""
