(set-logic LIA)

(synth-fun inv ((cmd Int) (snooze_timer Int) ) Bool)

(declare-var cmd Int)
(declare-var snooze_timer Int)


(constraint (= (inv cmd snooze_timer)
(and (>= 1 snooze_timer) (>= 2 cmd) (>= 1 cmd) (= 1 cmd) )
))

(check-synth)
