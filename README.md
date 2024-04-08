# slow-cdcl
Yet another inefficient and slow CDCL solver

### Dev Env Setup

- Install cvc5
`brew install cvc5` on MacOS or build your own using [installation instructions](https://cvc5.github.io/docs/cvc5-1.0.2/installation/installation.html)

- Python 3.12 (assumes virtualenv pyenv etc. is install)

```
$ virtualenv -p python cdcl-env
$ source cdcl-env/bin/activate
$ pip install -r requirements.txt
```

- check installation

```
$ python -i example.py
```

- run
``` 
python -i cdcl.py <filename>
```

#### Tests
- in the `tests` folder, just copied all the examples from from piazza/project description

## Todo

#### Input
- Proj 1 -      http://www.satcompetition.org/2009/format-benchmarks2009.html
- Proj 2/3: 
    - https://smtlib.cs.uiowa.edu/papers/smt-lib-reference-v2.6-r2021-05-12.pdf
    - pySMT to parse - http://www.pysmt.org/

#### Output
- Proj 1 - https://satcompetition.github.io/2024/output.html
- Proj 2/3 - Not sure, but i think same as above?

#### Proj 1 specific stuff


- Allowed to refer https://kienyew.github.io/CDCL-SAT-Solver-from-Scratch/, but if we do that, we have to add our own enhancements such as:
    - the Variable State Independent Decaying Sum (VSIDS) heuristic, to pick an unassigned
variable for Decide;
    - a Luby policy, or an arithmetic policy for Restart;
    - a time and space-efficient implementation using Numpy arrays instead of less efficient imple-
mentations such as dictionaries or maps.

- Two watched literals -  https://www.cs.upc.edu/~oliveras/LAI/cdcl.pdf
- VSIDS - https://www.princeton.edu/~chaff/publication/DAC2001v56.pdf  (Section 2 and 3)

- **Benchmarks/evaluation**
    - https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html
    - Benchmarks for final evaluation will be released later

#### Proj 2 specific stuff
- Build a CDCL resolution based solver
- Interface it with an off the shelf theory (LRA) solver

- **Benchmarks/evaluation**
    - https://smtlib.cs.uiowa.edu/benchmarks.shtml
    - Benchmarks for final evaluation will be released later

#### Proj 3 specific stuff
- https://www.cs.princeton.edu/courses/archive/spr08/cos226/lectures/01UnionFind.pdf
- https://www.cs.upc.edu/~oliveras/IC.pdf
- https://web.eecs.umich.edu/~weimerw/2011-6610/reading/nelson-oppen-congruence.pdf

- **Benchmarks/evaluation**
    - Have to make our own tests
    - Benchmarks for final evaluation will be released later
