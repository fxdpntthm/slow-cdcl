
# inspirations from pysmt docs
# https://pysmt.readthedocs.io/en/latest/tutorials.html#how-to-access-functionalities-of-solvers-not-currently-wrapped-by-pysmt

from pysmt.logics import QF_UFLRA, QF_UFIDL, QF_LRA, QF_IDL, QF_LIA
from pysmt.shortcuts import get_env, GT, Solver, Symbol, And, Or, Not, is_unsat, is_sat, get_unsat_core, get_model
from pysmt.typing import REAL
from pysmt.exceptions import NoSolverAvailableError
from pysmt.rewritings import conjunctive_partition

from IO import read_input

import sys
from os.path import exists


# SOLVER_NAME = "z3" # Note: The API version is called 'msat'
# SOLVER_PATH = ["/usr/local/bin/z3"] # Path to the solver
# SOLVER_LOGICS = [QF_LRA] # Some of the supported logics


def build_skeleton_map(formula):
    """
    Builds map to represent each literal.
    eg.     {1 -> x + y >= 0, 2 -> B, 3 -> D, 4 -> y <=0 , 5 -> C}
            and also its inverse map
            {x + y >= 0 -> 1, B -> 2, D -> 3, y <=0 -> 4, C -5}
    """
    atoms = formula.get_atoms()
    atom_map = {}
    atom_rev = {}
    i = 1
    for atom in atoms:
        atom_map[atom] = i
        atom_rev[i] = atom
        i += 1
    return (atom_map,atom_rev)

def build_skeleton(formula, atom_map):
    """
    The input formula is in CNF form and may contain theory literals,
       eg. (!(x + y >= 0) \/ B)  /\  ! D  /\   (y <= 0 \/ C)
    Computes the boolean skeleton of the formula:
       [[-1, 2], [-3] ,[4, 5]]

    the skel_map contains the mappings for atoms to numbers
    {x + y >= 0 -> 1, B -> 2, D -> 3, y <=0 -> 4, C -5}
    """
    formula_skeleton = []
    for clause in formula.args():
        # Each clause is either a literal, negated literal, OR atoms
        clause_skeleton = []
        if len(clause.args()) == 0:
            # this is a singleton clause so just append its lookup
            clause_skeleton.append(atom_map[clause])
        else:
            for literal in clause.args():
                if literal.is_not():
                    clause_skeleton.append(-1 * atom_map[literal.arg(0)])
                else: clause_skeleton.append(atom_map[literal])
        clause_skeleton.sort()
        formula_skeleton.append(clause_skeleton)
    return formula_skeleton

def build_formula(skeleton, atom_map):
    """
    inverse of build_skeleton function.
    Given a boolean skeleton and a reverse map of the atom_map
    return the QF_LRA formula.

    Eg. the input skeleton is:
                [[-1, 2], [-3] ,[4, 5]]

    the atom_map is:
               {1 -> x + y >= 0, 2 -> B, 3 -> D, 4 -> y <=0 , 5 -> C}

    returns (!(x + y >= 0) \/ B)  /\  ! D  /\   (y <= 0 \/ C)
    """
    clauses = []
    for c in skeleton:
        atoms = []
        for l in c:
            if l < 0:
                atoms.append(Not(atom_map[-1*l]))
            else:
                atoms.append(atom_map[l])
        clauses.append(Or(atoms))
    return And(clauses)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Error: No input file passed.")
    fpath = sys.argv[1]
    if not exists(fpath):
        sys.exit(f"Error: {fpath} does not exists.")

    # Build the FNode formula
    formula, free_vars = read_input(fpath)
    # build the skeleton map
    skel_map,rev_map = build_skeleton_map(formula)
    # build the skeleton
    skeleton = build_skeleton(formula, skel_map)

    # print("Clause Set: " + str(formula))
    # print("Atoms: " + str(formula.get_atoms()))
    # print("Atom map: " + str(skel_map))
    # print("Boolean skeleton: " + str(skeleton))

    with Solver(name="z3", logic="QF_LRA", unsat_cores_mode="all") as solver:
        solver.set_option(":produce-models", "true")

        solver.add_assertion(formula)
        sat = solver.solve()

        if sat:
            print("sat")
            m = solver.get_model()
            for v in free_vars:
                print(f"{v} := {m.get_value(v)}")
        else:
            print("unsat")
            ucore = solver.get_unsat_core()
            blocking_clause = And(list(ucore))
            # print(f"blocking clause = {blocking_clause}")
