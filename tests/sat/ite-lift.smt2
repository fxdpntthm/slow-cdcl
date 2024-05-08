;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress0/arith
;; Modified


(set-info :status sat)
(set-info :category "crafted")
(set-info :difficulty "0")
(set-logic QF_LRA)

(declare-fun x_0 () Real)
(declare-fun x_1 () Real)
(declare-fun x_2 () Real)
(assert (<= x_0 0))
(assert (<= x_1 0))
(assert (not (> x_2 0)))
(assert (>= (+ x_0 x_1) x_2))
(check-sat)
