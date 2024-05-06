
# inspirations from pysmt docs
# https://pysmt.readthedocs.io/en/latest/tutorials.html#how-to-access-functionalities-of-solvers-not-currently-wrapped-by-pysmt

from pysmt.logics import QF_UFLRA, QF_UFIDL, QF_LRA, QF_IDL, QF_LIA
from pysmt.shortcuts import get_env, GT, Solver, Symbol, And, Or, Not, is_unsat, is_sat, get_unsat_core, get_model
from pysmt.typing import REAL
from pysmt.exceptions import NoSolverAvailableError

from IO import read_input
from cdcl import solve

import sys
from os.path import exists
import time
from Model import Model
from Clause import Clause

import cProfile, pstats, io
from pstats import SortKey

import numpy as np

pr = cProfile.Profile()


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
        clause_skeleton = build_skeleton_clause(clause, atom_map)
        formula_skeleton.append(clause_skeleton)
    return formula_skeleton

def build_skeleton_clause(clause, atom_map):
    clause_skeleton = []
    # Each clause is either a literal, negated literal
    if len(clause.args()) == 0:
            # this is a singleton clause so just append its lookup
            clause_skeleton.append(atom_map[clause])
    else:
        for literal in clause.args():
            if literal.is_not():
                clause_skeleton.append(-1 * atom_map[literal.arg(0)])
            else: clause_skeleton.append(atom_map[literal])
        clause_skeleton.sort()
    return clause_skeleton

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
    with cProfile.Profile() as pr:

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
        # how many variables do we have?
        problem_size = len(skel_map)

        clause_set = []
        # make a list of Clause objects out of a list of ints
        for clause in skeleton:
            c = Clause(problem_size, clause)
            #print(f"list: {clause}, Clause: {c.data}")
            clause_set.append(c)

        # print("Clause Set: " + str(formula))
        # print("Atoms: " + str(formula.get_atoms()))
        # print("Atom map: " + str(skel_map))
        # print("Boolean skeleton: " + str(skeleton))



        t1 = time.time()
        with Solver(name="z3", logic="QF_LRA", unsat_cores_mode="all") as tsolver:
            while True:
                models = []
                # with  SatSolver() as ssolver:
                tsolver.set_option(":produce-models", "true")
                # print(f"Clause set: {clause_set.__str__()}")
                # TODO: skeleton should be a list of Clause objects
                sat_model = solve(clause_set, problem_size)
                assert len(list(filter(lambda x: x == sat_model, models))) == 0
                print("sat model: " + str(sat_model))
                models.append(sat_model)
                if sat_model is None:
                    t2 = time.time()
                    print("unsat")
                    break
                # print(f"sat model {sat_model}")
                # print(f"tsolver formula {And([build_formula([[l]], rev_map) for l in sat_model ])}")
                tsolver.push()
                tsolver.add_assertion(And([build_formula([[l]], rev_map) for l in sat_model ]))
                if tsolver.solve():
                    print("sat")
                    m = tsolver.get_model()
                    t2 = time.time()
                    for v in free_vars:
                        print(f"{v} := {m.get_value(v)}")
                    break
                else:
                    ucore = tsolver.get_unsat_core()
                    # blocking_clause = And(list(ucore))
                    blocking_clause = []
                    for c in ucore:
                        blocking_clause = Or(list(map(lambda x: Not(x), c.args())))
                        blocking_clause_skeleton = build_skeleton_clause(blocking_clause, skel_map)



                        skeleton.append(blocking_clause_skeleton)

                #blocking_clause_skeleton.sort()
                        blocking_clause = Clause(problem_size, init=blocking_clause_skeleton)
                        print(f"{ucore} {blocking_clause}")
                        assert len(list(filter(lambda x: blocking_clause.eq(x), clause_set))) == 0

                        clause_set.append(blocking_clause)
                #print(f"blocking clause: {len(blocking_clause_skeleton)} {blocking_clause_skeleton}")
                        tsolver.pop()
        sortby = SortKey.CUMULATIVE
        with open("perf-stats.txt", "w", encoding="utf-8") as s:
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
        print(t2 - t1)
