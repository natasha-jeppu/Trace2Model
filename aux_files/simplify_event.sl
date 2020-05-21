(set-logic LIA)
(synth-fun inv ((pump Bool)) Bool)

(declare-var pump Bool)

(constraint (= (inv pump) (not pump)))

(check-synth)