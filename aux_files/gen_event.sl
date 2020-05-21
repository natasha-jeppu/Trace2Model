(set-logic LIA)
(synth-fun next ((methane Int) ) Int
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
					 (>= Var Var)						
					 (<= Var Var)						
					 (and StartBool StartBool)			
					 (or  StartBool StartBool)				
					 (not StartBool)))))

(declare-var methane Int)


(constraint (= (next 551 ) 2))
(constraint (= (next 551 ) 2))
(constraint (= (next 562 ) 2))
(constraint (= (next 562 ) 2))
(constraint (= (next 571 ) 2))
(constraint (= (next 566 ) 2))
(constraint (= (next 554 ) 2))
(constraint (= (next 564 ) 2))
(constraint (= (next 565 ) 2))
(constraint (= (next 560 ) 2))
(constraint (= (next 548 ) 2))
(constraint (= (next 553 ) 2))
(constraint (= (next 565 ) 2))

(check-synth)
