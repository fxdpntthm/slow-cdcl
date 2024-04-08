;; problem.smt2
(set-logic QF_LRA)

(declare-fun a () Real)
(declare-fun b () Real)

(assert (<= a 5))
(assert (<= b a))

(assert (>= a 0))
(assert (>= b 0))

(check-sat)