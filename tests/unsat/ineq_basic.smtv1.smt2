;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress0/ineq_basic.smtv1.smt2
;; Modified

(set-option :incremental false)
(set-info :status unsat)
(set-logic QF_LRA)
(declare-fun x () Real)
(assert (<= 0.0 x))
(assert (< x 0.0))
(check-sat)
