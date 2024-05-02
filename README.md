# slow-cdcl
Yet another inefficient and slow CDCL solver

### Dev Env Setup

- Python <= 3.10 (assumes virtualenv pyenv etc. is install)

```
$ virtualenv -p python cdcl-env
$ source cdcl-env/bin/activate
$ pip install -r requirements.txt
$ pysmt-install --z3
```

- check installation

```
$ python -i example.py
```

- run
```
python main.py <filename>
```

#### Tests
- in the `tests` folder, just copied all the examples from from piazza/project description

### Project 2:

#### Tasks: Part A

1. Build a CDCL solver
   - Use an appropriate term representation of propositional logic.
   - Use the appropriate translation of the logic rules to come up with an assignment

#### Tasks: Part B
1. Interface the CDCL solver with the LIA theory formulas
2. Parse the smt-lib2 files and store them in an appropriate AST
3. Convert them to a Propositional logic formula
4. ask the CDCL solver if an assigment is possible
   - If it is satisfiable send it to the theory solver to come up with an assigment or output unsat
5. come up with an unsat core using z3



####  Notes:
- Allowed to refer https://kienyew.github.io/CDCL-SAT-Solver-from-Scratch/, but if we do that, we have to add our own enhancements such as:
    - the Variable State Independent Decaying Sum (VSIDS) heuristic, to pick an unassigned
variable for Decide;
    - a Luby policy, or an arithmetic policy for Restart;
    - a time and space-efficient implementation using Numpy arrays instead of less efficient implementations such as dictionaries or maps.

#### Input

- https://smtlib.cs.uiowa.edu/papers/smt-lib-reference-v2.6-r2021-05-12.pdf
- pySMT to parse - http://www.pysmt.org/

#### Output
Bunch of debug messages.
Final message is `sat` or `unsat`
In case of sat, a model is printed

`perf-stats.txt` shows performance stats
