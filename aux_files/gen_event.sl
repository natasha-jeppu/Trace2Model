(set-logic LIA)
(synth-fun next ((methane Int) (pump Bool) ) Int
	((Start Int (
				 2
				 (ite StartBool Start Start)))

	(Var Int (
			 1
			 2
			 7
			 559
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

(declare-var methane Int)
(declare-var pump Bool)


(constraint (= (next 551 true ) 2))
(constraint (= (next 551 true ) 2))
(constraint (= (next 562 true ) 2))
(constraint (= (next 562 true ) 2))
(constraint (= (next 571 true ) 2))
(constraint (= (next 566 true ) 2))
(constraint (= (next 554 true ) 2))
(constraint (= (next 564 true ) 2))
(constraint (= (next 565 true ) 2))
(constraint (= (next 560 true ) 2))
(constraint (= (next 548 true ) 2))
(constraint (= (next 553 true ) 2))
(constraint (= (next 565 true ) 2))

(check-synth)
