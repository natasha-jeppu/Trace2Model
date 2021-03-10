(set-logic LIA)
(synth-fun inv ((prev_inp.temp Int) (desiredTemperature Int) (allowedError Int) ) Bool)

(declare-var prev_inp.temp Int)
(declare-var desiredTemperature Int)
(declare-var allowedError Int)


(constraint (= (inv prev_inp.temp desiredTemperature allowedError) (and (>= prev_inp.temp (- desiredTemperature allowedError)) (not (= prev_inp.temp (- desiredTemperature allowedError))))))

(check-synth)