(set-logic LIA)
(synth-fun next ((pump Bool) ) Bool
	((Start Bool (
				 true
				 false
			 	 pump
				 (>= Start_Int Start_Int)						
				 (<= Start_Int Start_Int)						
				 (and Start Start)			
				 (or  Start Start)				
				 (not Start)))

	 (Start_Int Int (
					(+ Start_Int Start_Int)						
					(- Start_Int Start_Int)						
					(* Start_Int Start_Int)
					0
					1
					(ite Start Start_Int Start_Int)))))

(declare-var pump Bool)


(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))
(constraint (= (next true ) true))

(check-synth)
