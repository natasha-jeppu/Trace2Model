(set-logic LIA)
(synth-fun next ((pump Bool) ) Int
	((Start Int (
				 2
				 (ite StartBool Start Start)))

	(Var Int (
			 1
			 2
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

(declare-var pump Bool)


(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))
(constraint (= (next true ) 2))

(check-synth)
