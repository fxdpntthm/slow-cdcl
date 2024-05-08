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

    #print(f"Clauses: {list(map(lambda x: x.to_list(), clause_set))}")
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
    total_len = len(unresolved_clauses)

    # TODO: once restart is done, use restart instead of while true
    while len(unresolved_clauses) > 0 or conflict_clause is not None:
        #print(f"Model:\n{model.to_list()}\nUnresolved:\n{list(map(lambda x: x.to_list(), unresolved_clauses))}\nmodel complete:{model.is_complete()}\nconflict clause: {None if conflict_clause is None else conflict_clause.to_list()}")

        # run unit propagation as much as possible
        #####
        # Step 1.
        #####

        if conflict_clause is None:
            assert len(unresolved_clauses) + len(satisfied_clauses) == total_len, f"{(len(unresolved_clauses), len(satisfied_clauses), total_len)}"
            #print(f"unresolved clauses {len(unresolved_clauses), len(satisfied_clauses)}")
            (unresolved_clauses, new_unit_clauses, conflict_clause) = propagate_possible(unresolved_clauses, model)
            satisfied_clauses.extend(new_unit_clauses)
           # print(f"new unit clauses: {new_unit_clauses}")
            if len(new_unit_clauses) > 0:
                # it is possible that this propagate makes other unresolved clauses unit
                continue

            ####
            # Step 3
            ####
            # run decide as no propagation possible
            if not model.is_complete():
                model.decide()
            else:
                unresolved_clauses, new_sat_clauses, conflict_clause = model.check_clauses(unresolved_clauses)
                satisfied_clauses.extend(new_sat_clauses)
        else:
            #print("can no longer propogate")
            ####
            # Step 4.
            ####

            # if there's a failing clause and there are no decides left to reverse in the model
            # return UNSAT
            if not model.has_decide():
                #print(f"Unsat Model:\n{model}\nConflicting Clause:\n{conflict_clause}")
                return None


            #####
            # Step 5
            #####
            #print(f"Before explain\n{conflict_clause.to_list()}")
            conflict_clause = explain(unresolved_clauses + satisfied_clauses, model, conflict_clause)
            #print(f"Conflicting clause:\n{conflict_clause.to_list()} {len(conflict_clause.to_list())}")
            #print(f"Expalined conflicting clause:\n{conflict_clause}")
            # print(f"Explain:\n{conflict_clause}\ndelta:{unresolved_clauses + satisfied_clauses}\n---\n")
            for clause in unresolved_clauses + satisfied_clauses:
                if conflict_clause and clause.eq(conflict_clause):
                    # we have learned this clause already, so we have to have unsat at this point
                    print(f"WTF;trying to add a learned clause again\n{conflict_clause}in\n{unresolved_clauses + satisfied_clauses}")
                    return None

            #####
            # Step 6
            #####
            unresolved_clauses = learn_backjump(unresolved_clauses + satisfied_clauses, model, conflict_clause)
            unresolved_clauses, satisfied_clauses, conflict_clause = model.check_clauses(unresolved_clauses)
            assert conflict_clause is None
            #conflict_clause = None
            #print(f"after backjump: {unresolved_clauses}\nModel:\n{model}")


    # We have a model which satisfies all the clauses
    assert conflict_clause is None, f"conflict clause is not None {conflict_clause}"
    assert len(unresolved_clauses) == 0, f"unresolved clauses {unresolved_clauses}"

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


def propagate_possible(unresolved_clauses: list[Clause], model: Model) -> (list[Clause], list[Clause], Optional[Clause]):
    """
    Finds a unit literal and splits unresolved_clauses into resolved and unresolved clauses
    The model parameter is modified by the function
    """

    #print(f"unresolved clauses {unresolved_clauses}")
    literal = None
    for clause in unresolved_clauses:
        literal = model.makes_unit(clause)

        if literal is not None:
            model.add(literal)
            #print(f"Propagating {literal}...")
            return model.check_clauses(unresolved_clauses)
            # print("no Prop")
    return model.check_clauses(unresolved_clauses)

def explain(clause_set: list[Clause], model: Model, conflict_clause: Clause) -> Clause:
    """
    Modifies the conflict clause
    """

    cc_lits = conflict_clause.to_list()
    cc_lits.sort(key = lambda x: model.literal_lvls[-1*x])
    cc_lits.reverse()
    #print(f"conflict_clause: {conflict_clause.to_list()}")
    for lit in cc_lits:
        restof_cc =  Clause(conflict_clause.size, cc_lits)
        restof_cc.remove(lit)

        pivot = -1 * lit

        clauses_with_negl = list(filter(lambda x: x.has(pivot), clause_set))
        #print(f"\n---\nModel:\n{model.to_list()}\ndelta:\n{clause_set}\nconflict_clause:\n{cc_lits}")
        #print(f"d:\n{restof_cc.to_list()}\nclauses with {pivot}:\n{list(map(lambda x: x.to_list(), clauses_with_negl))}")
        
        # print(f"model: {model.to_list()}")

        for c in clauses_with_negl:

            copy_c = Clause(c.size)
            copy_c.copy(c)
            # print(f"copy_c: {copy_c}")
            copy_c.remove(pivot)
            neg_c = copy_c.negated()
            # print(f"candidate:\n{neg_c}")

            if model.contains_clause(neg_c):
                # print(f"m satisfies:\n{neg_c}\n---")

                restof_cc.data |= copy_c.data

                i = 1
                while i <= restof_cc.size:
                    if restof_cc.has(i) and restof_cc.has(-1*i):
                        continue
                    i += 1
                #print(f"new_explain_clause:\n{restof_cc.to_list()}")
                return restof_cc
    


def learn_backjump(clause_set: list[Clause], model: Model, conflict_clause: Clause):
    """
    adds clauses from the conflict_clause to the clause_set
    computes where to backjump and performs the backjump
    """
    assert conflict_clause is not None

    #print(f"In L&B Model:\n{model.to_list()}\ncc:\n{conflict_clause.to_list()}")

    levels = list(map(lambda x: (x, model.compute_level(-1*x)), conflict_clause.to_list()))
    #print(f"levels:{levels}")
    levels.sort(key=lambda x: x[1])
    backjump_level = levels[-2][1] if len(levels) > 1 else levels[0][1] - 1
    p_literal = levels[-1][0]

    #print(f"backjumping, level:{backjump_level} lit:{p_literal}")

    current = model.to_list()

    model.data = model.data[:backjump_level] if backjump_level > 0 else [model.data[0]]

    for literal in current:
        if not model.has(literal):
            del model.literal_lvls[literal]

    # print(f"Model:{model.data}")
    model.add(p_literal)
    #clause_set.append(conflict_clause)

    return clause_set


"""
clause = [0, 1,2,.... -2,-1]
"""
