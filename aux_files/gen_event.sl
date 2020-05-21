(set-logic LIA)
(synth-fun next ((water Int) (methane Int) (pump Bool) ) Int
	((Start Int (
				 2
			 (ite StartBool Start Start)))

	(Var Int (
				 0
				 1
				 2
				 7
				 29
				 559
				 water
				 methane
				 (+ Var Var)						
				 (- Var Var)						
				 (* Var Var)))

	 (StartBool Bool (
				 	 pump
					 (>= Var Var)						
					 (<= Var Var)						
					 (and StartBool StartBool)			
					 (or  StartBool StartBool)				
					 (not StartBool)))))

(declare-var water Int)
(declare-var methane Int)
(declare-var pump Bool)


(constraint (= (next 29 551 true ) 2))
(constraint (= (next 29 551 true ) 2))
(constraint (= (next 29 562 true ) 2))
(constraint (= (next 29 562 true ) 2))
(constraint (= (next 30 571 true ) 2))
(constraint (= (next 29 566 true ) 2))
(constraint (= (next 29 554 true ) 2))
(constraint (= (next 30 564 true ) 2))
(constraint (= (next 29 565 true ) 2))
(constraint (= (next 29 560 true ) 2))
(constraint (= (next 29 548 true ) 2))
(constraint (= (next 29 553 true ) 2))
(constraint (= (next 29 565 true ) 2))

(check-synth)
