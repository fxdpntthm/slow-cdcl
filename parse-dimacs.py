""" 
Simple DIMACS parser script to run just the sat solver separately on DIMACS files
Using this to test whether the SAT solver is working correctly
Adapted from - https://kienyew.github.io/CDCL-SAT-Solver-from-Scratch/The-Implementation.html

How to run - 
python parse-dimacs.py <filename>
"""

import sys
from cdcl import solve

def parse_dimacs_cnf(content: str):
    """
    parse the DIMACS cnf file format into corresponding Formula.
    """
    clauses = [[]]
    for line in content.splitlines():
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            for tok in tokens:
                lit = int(tok)
                if lit == 0:
                    clauses.append([])
                else:
                    clauses[-1].append(lit)

    if len(clauses[-1]) == 0:
        clauses.pop()

    return clauses

if len(sys.argv) < 2:
    print("No file given")
    sys.exit()

fname = sys.argv[1]

content = str(open(fname,"r").read())

clause_set = parse_dimacs_cnf(content)
print(clause_set)
print()
print(solve(clause_set))