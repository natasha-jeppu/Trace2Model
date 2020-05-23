(set-logic LIA)
(synth-fun next ((ip Int) (op Int) ) Int
	((Start Int (
				 (+ Start Start)						
				 (- Start Start)						
				 (* Start Start)
				 ip
				 op
				 0
				 1
				 (ite StartBool Start Start)))

	 (StartBool Bool (
					 (>= Start Start)						
					 (<= Start Start)						
					 (and StartBool StartBool)			
					 (or  StartBool StartBool)				
					 (not StartBool)))))

(declare-var ip Int)
(declare-var op Int)


(constraint (= (next 1 -4 ) -3))
(constraint (= (next 1 -3 ) -2))
(constraint (= (next 1 -2 ) -1))

(check-synth)
