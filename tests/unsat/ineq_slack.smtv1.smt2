;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress0
;; Modified

(set-option :incremental false)
(set-info :status unsat)
(set-logic QF_LRA)
(declare-fun x () Real)
(declare-fun y () Real)
(assert (<= (+ x y) 0.0))
(assert (and (< 1.0 x) (<= 0.0 y)))
(check-sat)