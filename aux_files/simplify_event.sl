(set-logic LIA)
(synth-fun inv ((methane Int)) Bool)

(declare-var methane Int)

(constraint (= (inv methane) (>= methane (+ 16 565))))

(check-synth)