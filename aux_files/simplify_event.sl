(set-logic LIA)
(synth-fun inv ((methane Int)) Bool)

(declare-var methane Int)

(constraint (= (inv methane) (and (>= 609 (+ 2 methane))(not (>= methane 609)))))

(check-synth)