(set-logic LIA)
(synth-fun next ((methane Int) (pump Bool) ) Int
	((Start Int (
				 1
				 7
				 (ite StartBool Start Start)))

	(Var Int (
			 1
			 2
			 22
			 577
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


(constraint (= (next 571 false ) 1))
(constraint (= (next 583 false ) 1))
(constraint (= (next 597 false ) 1))
(constraint (= (next 603 false ) 7))
(constraint (= (next 599 false ) 1))
(constraint (= (next 584 false ) 1))
(constraint (= (next 583 false ) 1))
(constraint (= (next 563 false ) 1))
(constraint (= (next 545 false ) 1))
(constraint (= (next 541 false ) 1))

(check-synth)
