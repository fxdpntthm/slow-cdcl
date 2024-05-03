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
    3. Decide on a literal
    4. Check for conflicts
    5. If there is a conflict, compute the conflict clause
    6. Learn the conflict clause, and backjump
    7. go to step 1
    """

    # print(f"Start of solver: {model}\n{clause_set[0]}")

    (unresolved_clauses, satisfied_clauses) = clause_set
    conflict_clause = None


    # TODO: once restart is done, use restart instead of while true
    while len(unresolved_clauses) > 0:
        # print(f"Model:\n{model}\nUnresolved:\n{unresolved_clauses}")

        # run unit propagation as much as possible
        #####
        # Step 1.
        #####
        (unresolved_clauses, new_unit_clauses) = propagate_possible(unresolved_clauses, model)
        # print(f"After propagation: {still_unresolved_clauses}, {new_unit_clauses}")
        satisfied_clauses.extend(new_unit_clauses)

        if len(new_unit_clauses) > 0:
            # it is possible that this propagate makes other unresolved clauses unit
            continue

        ####
        # Step 3
        ####
        # run decide as no propogation possible
        model.decide()

        unresolved_clauses, resolved = model.check_clauses(unresolved_clauses)

        satisfied_clauses.extend(resolved)

        # if len(unresolved_clauses) == 0:
        #     return model.to_list()

        ####
        # Step 4.
        ####
        conflicting_clause = check_falsify(unresolved_clauses,model)

        # if conflicting_clause: print(f"Model:\n{model}\nConflicting Clause:\n{conflicting_clause}")
        # if there's a failing clause and there are no decides left to reverse in the model
        # return UNSAT
        if conflicting_clause and (not model.has_decide()):
            print(f"Unsat Model:\n{model}\nConflicting Clause:\n{conflicting_clause}")
            return None

        if conflicting_clause:

            #####
            # Step 5
            #####
            conflict_clause = explain(unresolved_clauses + satisfied_clauses, model, conflicting_clause)
            # print(f"\n---\nModel:\n{model}\nConflicting clause:\n{conflicting_clause}")
            print(f"Explain:\n{conflict_clause}\ndelta:{unresolved_clauses + satisfied_clauses}\n---\n")
            for clause in unresolved_clauses + satisfied_clauses:
                if np.array_equal(conflict_clause.data,clause.data):
                    # we have learned this clause already, so we have to have unsat at this point
                    print(f"WTF;trying to add a learned clause again\n{conflict_clause}in\n{unresolved_clauses + satisfied_clauses}")
                    return None

            #####
            # Step 6
            #####
            new_clause_set = learn_backjump(unresolved_clauses + satisfied_clauses, model, conflict_clause)
            print(f"after backjump: {new_clause_set}\nModel:\n{model}")
            conflict_clause = None

            unresolved_clauses, satisfied_clauses = model.check_clauses(new_clause_set)

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
            model.add(literal)
            print(f"Propagating {literal}...")
            return model.check_clauses(unresolved_clauses)
            # print("no Prop")
    return (unresolved_clauses,[])


def explain(clause_set: list[Clause], model: Model, conflict_clause: Clause) -> Clause:
    """
    Modifies the conflict clause
    """
    cc_lits = conflict_clause.to_list()
    cc_lits.sort(key = lambda x: model.literal_lvls[-1*x])
    cc_lits.reverse()
    for lit in cc_lits:
        restof_cc =  Clause(conflict_clause.size, cc_lits)
        restof_cc.remove(lit)

        pivot = -1 * lit

        clauses_with_negl = list(filter(lambda x: x.has(pivot), clause_set))
        # print(f"\n---\nModel:\n{model}\ndelta:\n{clause_set}\nconflict_clause:\n{cc_lits}")
        # print(f"d:\n{restof_cc}\nclauses with {pivot}:\n{list(map(lambda x: x.to_list(), clauses_with_negl))}")
        for c in clauses_with_negl:
            copy_c = Clause(c.size)
            copy_c.copy(c)
            # print(f"copy_c: {copy_c}")
            copy_c.remove(pivot)
            neg_c = copy_c.negated()
            # print(f"candidate:\n{neg_c}")

            if all([model.has(l) for l in neg_c.to_list()]):
                # print(f"m satisfies:\n{neg_c}\n---")
                inconsistent = False
                for l in copy_c.to_list():
                    if restof_cc.consistent(l):
                        restof_cc.add(l)
                    else:
                        inconsistent = True
                        break
                # print(f"new conflict_clause: {restof_cc}")
                if inconsistent:
                    continue

                #print(f"new_explain_clause: {restof_cc.to_list()}")
                return restof_cc

def learn_backjump(clause_set: list[Clause], model: Model, conflict_clause: Clause):
    """
    adds clauses from the conflict_clause to the clause_set
    computes where to backjump and performs the backjump
    """

    clause_set.append(conflict_clause)

    # print(f"In L&B Model:\n{model.data}\ncc:\n{conflict_clause.to_list()}")

    levels = list(map(lambda x: (x, model.compute_level(-1*x)), conflict_clause.to_list()))
    # print(f"levels:{levels}")
    levels.sort(key=lambda x: x[1])
    backjump_level = levels[-2][1] if len(levels) > 1 else levels[0][1] - 1
    p_literal = levels[-1][0]

    print(f"backjumping, level:{backjump_level} l:{p_literal}")

    model.data = model.data[:backjump_level] if backjump_level > 0 else [model.data[0]]
    # print(f"Model:{model.data}")
    model.add(p_literal)

    return clause_set


"""
clause = [0, 1,2,.... -2,-1]
"""
