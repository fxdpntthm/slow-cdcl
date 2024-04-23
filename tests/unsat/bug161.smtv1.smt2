;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress0
;; Modified

(set-option :incremental false)
(set-info :status unsat)
(set-logic QF_LRA)
(declare-fun x_1 () Real)
(assert (and (= x_1 10.0) (< x_1 1.0)))
(check-sat)
