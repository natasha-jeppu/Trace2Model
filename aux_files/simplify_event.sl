(set-logic LIA)
(synth-fun inv ((methane Int)) Bool)

(declare-var methane Int)

(constraint (= (inv methane) (and (>= 31 (* (- methane 589)  2)) (>= methane 589))))

(check-synth)