;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress0
;; Modified

(set-option :incremental false)
(set-logic QF_LRA)
(declare-fun x_34 () Real)
(declare-fun x_13 () Real)
(declare-fun x_30 () Real)
(declare-fun x_59 () Real)
(assert (and (not (<= x_59 0.0)) (= x_30 x_59) (= x_30 0.0) (or false (= x_13 x_34))))
(check-sat)
