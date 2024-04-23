;; example.smt2
(set-logic QF_LRA)

(declare-fun x () Real)

(assert (or (< x 0) (> x 0)))

(check-sat)
(get-model)