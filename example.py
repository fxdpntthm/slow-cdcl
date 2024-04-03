import cvc5

solver = cvc5.Solver()
solver.setOption("produce-models", "true")
solver.setOption("produce-unsat-cores", "true")
solver.setOption("minimal-unsat-cores", "true")
solver.setOption("incremental", "true")

Int = solver.getIntegerSort()

LT = cvc5.Kind.LT
GT = cvc5.Kind.GT
EQUAL = cvc5.Kind.EQUAL
ADD = cvc5.Kind.ADD
MULT = cvc5.Kind.MULT

_0 = solver.mkInteger(0)
_2 = solver.mkInteger(2)

x = solver.mkConst(Int, "x")
y = solver.mkConst(Int, "y")

x_lt_0 = solver.mkTerm(LT, x, _0)
x_gt_0 = solver.mkTerm(GT, x, _0)
x_eq_2y = solver.mkTerm(EQUAL, x, solver.mkTerm(ADD, y, y))

solver.assertFormula(x_lt_0)
solver.assertFormula(x_gt_0)
solver.assertFormula(x_eq_2y)

res = solver.checkSat()

print(res.isUnknown())

unsat_core = solver.getUnsatCore()

if x_lt_0 in unsat_core: print("x_lt_0")
if x_gt_0 in unsat_core: print("x_gt_0")
if x_eq_2y in unsat_core: print("x_eq_2y")
