;; Repository https://github.com/cvc5/cvc5
;; Folder cvc5/test/regress/cli/regress1/push-pop
;; Modified

(set-logic QF_LRA)
(set-info :status sat)
(declare-fun x0 () Real)
(declare-fun x1 () Real)
(declare-fun x2 () Real)
(assert (or (= (+ (* 40 x1 ) (* (- 35) x0 ) (* 10 x1 ) ) 4) (not (= (+ (* 38 x1 ) (* 40 x1 ) (* (- 28) x2 ) ) 44)) (< (+ (* (- 46) x1 ) (* (- 18) x0 ) ) 37) ))
(assert (or (<= (+ (* (- 4) x2 ) (* (- 29) x1 ) ) (- 37)) (not (> (+ (* (- 10) x2 ) (* 13 x0 ) ) (- 21))) ))
(assert (or (> (+ (* 21 x0 ) (* 13 x2 ) ) 49) (>= (+ (* 19 x2 ) (* 45 x2 ) (* 9 x1 ) ) (- 45)) ))
(assert (or (= (+ (* (- 17) x0 ) (* 22 x0 ) ) 12) (<= (+ (* 28 x1 ) (* 27 x0 ) (* 39 x0 ) (* (- 49) x2 ) ) (- 9)) ))
(assert (or (not (<= (+ (* (- 49) x2 ) (* (- 28) x1 ) (* 24 x2 ) ) 47)) (>= (+ (* 13 x2 ) (* 49 x0 ) (* (- 45) x0 ) (* (- 44) x1 ) ) (- 14)) ))
(assert (or (> (+ (* 9 x1 ) (* 18 x2 ) ) 31) (not (<= (+ (* 10 x2 ) (* 49 x1 ) (* (- 29) x2 ) (* (- 45) x2 ) ) (- 22))) ))
(assert (not (<= (+ (* 49 x0 ) (* (- 50) x0 ) (* 0 x1 ) ) 40)) )
(assert (or (> (+ (* 37 x1 ) (* (- 37) x2 ) ) (- 13)) (not (< (+ (* (- 38) x2 ) (* (- 15) x2 ) (* (- 39) x2 ) (* (- 13) x1 ) ) 20)) (>= (+ (* 8 x2 ) (* 47 x1 ) (* (- 21) x2 ) (* 41 x0 ) ) 13) ))
(assert (or (> (+ (* (- 26) x2 ) (* 9 x0 ) (* (- 47) x1 ) (* (- 30) x0 ) ) (- 12)) (not (>= (+ (* 3 x0 ) (* 24 x0 ) ) (- 10))) ))
(assert (< (+ (* (- 41) x1 ) (* (- 42) x1 ) (* 41 x1 ) ) (- 36)) )
(check-sat)
