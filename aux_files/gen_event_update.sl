(set-logic LIA)

(declare-datatypes ((c_t 0))
	(((on) (off))))

(synth-fun next ((s c_t) ) c_t
	((Start c_t) (StartBool Bool))
	((Start c_t (
					s
					on
					off
					(ite StartBool Start Start)))

	(StartBool Bool (
				 (= Start Start)
				 true
				 false				
				 (and StartBool StartBool)			
				 (or  StartBool StartBool)				
				 (not StartBool)))
		))

(declare-var s c_t)


(constraint (= (next on ) off))
(constraint (= (next off ) on))
(constraint (= (next on ) off))

(check-synth)
