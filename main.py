
# inspirations from pysmt docs
# https://pysmt.readthedocs.io/en/latest/tutorials.html#how-to-access-functionalities-of-solvers-not-currently-wrapped-by-pysmt

from pysmt.logics import QF_UFLRA, QF_UFIDL, QF_LRA, QF_IDL, QF_LIA
from pysmt.shortcuts import get_env, GT, Solver, Symbol, And, Or, Not
from pysmt.typing import REAL
from pysmt.exceptions import NoSolverAvailableError

from IO import read_input

import sys



SOLVER_NAME = "mathsat" # Note: The API version is called 'msat'
SOLVER_PATH = ["/usr/local/bin/cvc5"] # Path to the solver
SOLVER_LOGICS = [QF_UFLRA] # Some of the supported logics


env = get_env()
env.factory.add_generic_solver(SOLVER_NAME, SOLVER_PATH, SOLVER_LOGICS)

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
        print("no input file passed")
        sys.exit()
    else:
        formula = read_input(sys.argv[1])
        skel_map,rev_map = build_skeleton_map(formula)
        skeleton = build_skeleton(formula, skel_map)

        print("Clause Set: " + str(formula))
        print("Atoms: " + str(formula.get_atoms()))
        print("Atom map: " + str(skel_map))
        print("Boolean skeleton: " + str(skeleton))


        with Solver(name=SOLVER_NAME, logic=QF_LRA) as slvr:
            res = slvr.solve()
            assert res, "was expecting '%s' to be SAT" % formula
