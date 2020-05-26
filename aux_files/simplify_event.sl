(set-logic LIA)
(synth-fun inv ((methane Int)) Bool)

(declare-var methane Int)

(constraint (= (inv methane) (>= (+ 22 577)  methane)))

(check-synth)