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



    # TODO: once restart is done, use restart instead of while true
    while len(unresolved_clauses) > 0:
        # print(f"Model:\n{model}\nUnresolved:\n{unresolved_clauses}")

        # run unit propagation as much as possible
        (still_unresolved_clauses, new_unit_clauses) = propagate_possible(unresolved_clauses, model)
        # print(f"After propagation: {still_unresolved_clauses}, {new_unit_clauses}")
        unresolved_clauses = still_unresolved_clauses
        satisfied_clauses.extend(new_unit_clauses)

        if len(new_unit_clauses) > 0:
            # it is possible that this propagate makes other unresolved clauses unit
            continue

        # run decide
        decide_lit = decide_literal(model)
        print(f"decide {decide_lit}")
        # print(f"Model: {model.data[-1]}")

        if decide_lit == 0:
            continue # AI: I still think this is wrong and we should never reach this stage
            # if decide literal, decided on everything that is possible


        model.add_decide(decide_lit)

        unresolved, resolved = [], []

        for clause in unresolved_clauses:
            if model.satisfies_clause(clause):
                resolved.append(clause)
            else:
                unresolved.append(clause)


        unresolved_clauses = unresolved
        satisfied_clauses.extend(resolved)

        # get a failing clause, if any
        conflicting_clause = check_falsify(unresolved_clauses,model)

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
            learn_clause = conflict_clause.negated()

            for clause in unresolved_clauses + satisfied_clauses:
                if np.array_equal(learn_clause.data,clause.data):
                    # we have learned this clause already, so we have to have unsat at this point
                    print(f"trying to add a learned clause again {learn_clause}")
                    return None

            #print(f"Model before learn: {model.data}")
            unresolved_clauses.append(learn_clause)
            print(f"learned clause {learn_clause}")
            #print(f"Clause set: {list(map(lambda x: x.to_list(), clause_set))}")
            (backjump_level, negating_literal) = model.compute_backjump_level(learn_clause)
            print(f"backjump_level: {backjump_level}, negating_literal {negating_literal}")
            model.pop_n(backjump_level,negating_literal)
            conflict_clause = None
            unresolved_clauses.extend(satisfied_clauses)
            satisfied_clauses = [] # forget all the satisfying clauses



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
        print(f"Propagated\n{model}")
        for clause in unresolved_clauses:
            if model.satisfies_clause(clause):
                resolved.append(clause)
            else:
                unresolved.append(clause)

        return (unresolved, resolved)
    else:
        return (unresolved_clauses,[])




"""
    while True:
        unit_literal = None
        clause_unit = None
        for clause in unresolved_clauses:

            literal = model.makes_unit(clause)
            # print(f"makes_unit\n{model.data[-1]}\n{clause} {makes_unit} {literal}")
            if literal:
                clause_unit = clause
                unit_literal = literal
                resolved.append(clause)
                break
            else:
                unresolved.append(clause)

        # if there is a unit literal, add it to the model
        if unit_literal != None:
            model.add(unit_literal)

            resolved.append(clause_unit)
            print(f"Model after propagation:\n{model.data[-1]}")
            print(f"Unit clause:\n{clause_unit}")
        else:
            break

    return (unresolved,resolved)
"""

def backtrack_dpll(model: Model):
    """
    DPLL backtrack (just reverses the latest decide)
    The model parameter is modified by this function
    """

    top = model.pop_decide()
    if top == 0:
        print("Error: backtracking when you shouldn't be...")
        print(model.print())
        sys.exit()

    model.add(-1 * top)

def decide_literal(model: Model) -> int:
    """
    Returns the first unassigned literal
    """

    i = 1
    while i <= model.size:
        if not (model.has(i) or model.has(-1*i)):
            return i
        i += 1

    return 0

    # for clause in clause_set:
    #     i = 1
    #     while i <= clause.size:
    #         if clause.data[i] == 1 or clause.data[-1 * i] == 1:
    #             if not model.has(i) and not model.has(-1 * i):
    #                 decide_lit = i
    #                 break

    #         i += 1

    # if decide_lit == None:
    #     print("Cant decide anything...")
    #     return 0

    # return decide_lit

def decide(clause_set, delta, model, conflict_clause):
    """
    Generates a decision point in the model keeps track of where to back jump?
    """
    return (clause_set, delta, model, conflict_clause)

def conflict(clause_set: list[Clause], model: Model, conflict_clause: Optional[Clause]):
    """
    Checks if a conflict exists and if it does, adds a conflict clause.
    Otherwise just returns the passed parameters
    """

    return (clause_set, model, conflict_clause)

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
