import sys

"""
The main file that gives an assignment to a Propositional Boolean Logic formula in a CNF format
or returns UNSAT
"""


def solver (clause_set):
    """
    The solver takes a formula or the clause_set
    of a list of lists. The inner list are the set of literals.

    the clause set [[1,-2,3], [2,3], [2], [-1, 2]]
    represents the formula
    [(A \/ -B \/ C) /\  (B \/ C) /\  B /\ (-A \/ B)]

    """
    return "UNSAT"


"""
1 |-> x + y <= 0
2 |-> 4*x + z <= 1
"""


def solver_step(clause_set, delta, model, conflict_clause):
    """
    decides which rule to apply, returns the modified, clause_set, model, delta and C
    """
    if propgate_possible(clause_set):
        return propogate(clause_set, delta, model, conflict_clause)

    else: return (clause_set, delta, model, conflict_clause)

def propgate_possible(clause_set):
    """
    Checks if there's a single literal clause in the clause set
    """
    return False


def propogate(clause_set, delta, model, conflict_clause):
    """
    Applies propogate on the clause set
    """
    return (clause_set, delta, model, conflict_clause)

def decide(clause_set, delta, model, conflict_clause):
    """
    Generates a decision point in the model keeps track of where to back jump?
    """
    return (clause_set, delta, model, conflict_clause)


def explain(clause_set, delta, model, conflict_clause):
    """
    Modifies the conflict clause
    """
    return (clause_set, delta, model, conflict_clause)



def backjump(clause_set, delta, model, conflict_clause):
    """
    backjumps to an appropriate decision point.
    """
    return (clause_set, delta, model, conflict_clause)
