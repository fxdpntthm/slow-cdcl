import sys

from Model import Model
from typing import *

"""
The main file that gives an assignment to a Propositional Boolean Logic formula in a CNF format
or returns UNSAT
"""

def solve (clause_set: list[list[int]]) -> Optional [list[int]]:
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
    delta = []
    model = Model()
    conflict_clause = []

    # once restart is done, restart instead of while true
    while True:

        # if the current model satisifies the clause set, return it
        if sat(clause_set,model):
            return model.get_data()


        # get a failing clause, if any
        failing_clause = check_falsify(clause_set,model)

        # if there's a failing clause and there are no guesses left to reverse in the model,
        # return UNSAT
        if failing_clause != None and model.has_decide() == False:
            #print("Failing out...")
            #print(model.get_data())
            return None

        # if there is a failing clause and there is a guess that can be backtracked on,
        # run backtrack. currently just dpll backtrack,
        #  but conflict/explain/learn/backjump here in CDCL
        if failing_clause != None:
            backtrack_dpll(model)
            continue

        # run unit propagation as much as possible
        model_changed = propagate_possible(clause_set, model)
        if model_changed:
            continue

        # run decide
        decide_lit = decide_literal(clause_set,model)
        if decide_lit != 0:
            model.add_decide(decide_lit)
        else:
            break




"""
1 |-> x + y <= 0
2 |-> 4*x + z <= 1
"""


"""
RULES
Are we implementing RESTART?
"""


def sat(clause_set : list[list[int]], model: Model) -> bool:
    """
    Returns true if all clauses in a clause set is satisfied by the current model
    """
    for clause in clause_set:
        sat = False
        for lit in clause:
            if model.has(lit):
                sat = True
                break
    return sat

def check_falsify(clause_set: list[list[int]], model: Model) -> Optional[list[int]]:
    """
    Returns the first clause in a clause set where
    the model has a negated assignment for every literal in that clause set
    If none exist, returns None
    """
    for clause in clause_set:
        negated_set = set(list(map(lambda x: x * -1, clause)))

        if negated_set <= model.set():
            return clause

    return None

def propagate_possible(clause_set: list[list[int]], model: Model) -> bool:
    """
    Runs unit propagation as much as possible and returns whether the model was modified
    The model parameter is modified by the function
    """

    model_set = model.set()
    # a clause set where each clause is the negation of a clause of the passed-in clause set
    negated_clauses = list(map(lambda clause: list(map(lambda x: x * -1, clause)), clause_set))
    # sets for each negated clause set
    negated_sets = list(map(lambda clause: set(clause), negated_clauses))

    model_change = False

    while True:
        unit_clause = float("inf")

        for i in range(len(clause_set)):
            clause = clause_set[i]
            #negated clause
            negated = negated_clauses[i]
            negated_set = negated_sets[i]

            for j in range(len(clause)):
                # literal and negation not in the model, and negation of everything else in the model
                if ((clause[j] not in model_set)
                    and (negated[j] not in model_set)
                    and ((negated_set - set([negated[j]])) <= model_set)):
                    unit_clause = min(clause[j],unit_clause)

        # if there is a unit literal, add it to the model and model set
        if unit_clause != float("inf"):
            model.add(unit_clause)
            model_set.add(unit_clause)
            model_change = True
        else:
            break

    return model_change


def backtrack_dpll(model):
    """
    DPLL backtrack (just reverses the latest decide)
    """

    top = model.pop_decide()
    if top == 0:
        print("Error: backtracking when you shouldn't be...")
        print(model.print())
        return

    model.add(-1 * top)

def decide_literal(clause_set,model):
    """
    Returns the smallest unassigned literal
    """
    decide_lit = float("inf")
    for clause in clause_set:
        for literal in clause:
            if not model.has(literal) and not model.has(-1 * literal):
                if abs(literal) < abs(decide_lit):
                    decide_lit = literal

    if decide_lit == float("inf"):
        print("Cant decide anything...")
        return 0

    return decide_lit


def decide(clause_set, delta, model, conflict_clause):
    """
    Generates a decision point in the model keeps track of where to back jump?
    """
    return (clause_set, delta, model, conflict_clause)

def conflict(clause_set, delta, model, conflict_clause):
    """
    Checks if a conflict exists and if it does, adds a conflict clause.
    Otherwise just returns the passed parameters
    """
    return (clause_set, delta, model, conflict_clause)

def explain(clause_set, delta, model, conflict_clause):
    """
    Modifies the conflict clause
    """
    return (clause_set, delta, model, conflict_clause)

def fail(clause_set, delta, model, conflict_clause):
    """
    checks if a clause set is unsatisfiable
    """
    return (clause_set, delta, model, conflict_clause)

def learn(clause_set, delta, model, conflict_clause):
    """
    adds clauses from the conflict_clause to the clause_set
    """
    return (clause_set, delta, model, conflict_clause)


"""
clause = [0, 1,2,.... -2,-1]
"""
