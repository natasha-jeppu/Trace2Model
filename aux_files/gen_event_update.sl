(set-logic LIA)
(synth-fun next ((x Int) ) Int
	((Start Int (
				 (+ Start Start)						
				 (- Start Start)						
				 (* Start Start)
				 x
				 0
				 1
				 (ite StartBool Start Start)))

	 (StartBool Bool (
					 (>= Start Start)						
					 (<= Start Start)						
					 (and StartBool StartBool)			
					 (or  StartBool StartBool)				
					 (not StartBool)))))

(declare-var x Int)


(constraint (= (next 0 ) 0))

(check-synth)
