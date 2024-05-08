;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress0/arith
;; Modified

(set-info :status sat)
(set-logic QF_LRA)
(declare-fun tmp1 () Real)
(declare-fun x177 () Bool)
(assert (and (=> (and (not x177) true) (= tmp1 0.0)) (=> (and x177 true) (= tmp1 (/ (- 350) 1)))))
(check-sat)
