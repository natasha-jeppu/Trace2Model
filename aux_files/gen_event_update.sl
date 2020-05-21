(set-logic LIA)
(synth-fun next ((water Int) (pump Bool) ) Bool
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
					water
					0
					1
					(ite Start Start_Int Start_Int)))))

(declare-var water Int)
(declare-var pump Bool)


(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 30 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 30 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))
(constraint (= (next 29 true ) true))

(check-synth)
