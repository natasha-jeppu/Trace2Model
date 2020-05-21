(set-logic LIA)
(synth-fun next ((water Int) ) Int
	((Start Int (
				 2
			 (ite StartBool Start Start)))

	(Var Int (
				 0
				 1
				 2
				 29
				 water
				 (+ Var Var)						
				 (- Var Var)						
				 (* Var Var)))

	 (StartBool Bool (
					 (>= Var Var)						
					 (<= Var Var)						
					 (and StartBool StartBool)			
					 (or  StartBool StartBool)				
					 (not StartBool)))))

(declare-var water Int)


(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 30 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 30 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))
(constraint (= (next 29 ) 2))

(check-synth)
