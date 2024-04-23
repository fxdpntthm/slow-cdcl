;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress0

(set-logic QF_LRA)
(set-info :status sat)
(declare-fun x () Real)
(declare-fun y () Real)
(assert (not (= x (ite true y x))))
(check-sat)
