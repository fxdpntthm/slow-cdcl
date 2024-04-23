;; example.smt2
(set-logic QF_LRA)

(declare-fun x () Real)

(assert (< x 0))
(assert (> x 0))

(check-sat)
(get-model)