;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress1/push-pop
;; Modified

(set-logic QF_LRA)
(set-info :status sat)
(declare-fun x0 () Real)
(declare-fun x1 () Real)
(declare-fun x2 () Real)
(assert (< (+ (* 23 x1 ) (* (- 27) x1 ) (* 22 x0 ) ) (- 22)) )
(assert (>= (+ (* (- 4) x0 ) (* (- 9) x1 ) (* (- 40) x0 ) (* 40 x2 ) ) (- 27)) )
(assert (or (not (>= (+ (* (- 34) x0 ) (* (- 36) x1 ) ) (- 26))) (not (>= (+ (* 6 x2 ) (* (- 6) x1 ) ) (- 43))) ))
(assert (or (>= (+ (* 20 x2 ) (* 12 x0 ) (* (- 50) x1 ) ) (- 46)) (not (> (+ (* 11 x1 ) (* (- 30) x0 ) ) (- 21))) ))
(check-sat)