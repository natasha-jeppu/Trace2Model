(set-logic LIA)
(declare-datatypes ((inp.cmd_t 0))
	(((NO_CMD) (UNSHEL) (c_ACK) (c_SHEL) (c_SUPR) )))
(declare-datatypes ((prev_out.prev_s_t 0))
	(((NORMAL) (RTN_UNACK) (UNACK) (s_ACK) )))
(synth-fun next ((inp.val Int) (inp.cmd inp.cmd_t)(out.snooze_timer Int) (snooze_timeout Int) (high_thresh Int) (low_thresh Int) (prev_out.prev_s prev_out.prev_s_t)) Int
	((Start Int)  (Var Int) (EnumVar0 inp.cmd_t) (EnumVar1 prev_out.prev_s_t) (StartBool Bool))
	((Start Int (
				 0
				 1
				 (ite StartBool Start Start)))

	(Var Int (
				 1
			 inp.val
			 out.snooze_timer
			 snooze_timeout
			 high_thresh
			 low_thresh
			 	(+ Var Var)						
			 	(- Var Var)						
			 	(* Var Var)))

(EnumVar0 inp.cmd_t (
	inp.cmd
NO_CMD
UNSHEL
c_ACK
c_SHEL
c_SUPR
))

(EnumVar1 prev_out.prev_s_t (
	prev_out.prev_s
NORMAL
RTN_UNACK
UNACK
s_ACK
))

	 (StartBool Bool (
	 ( = EnumVar0 EnumVar0)
	 ( = EnumVar1 EnumVar1)
					 (> Var Var)						
					 (>= Var Var)						
					 (< Var Var)						
					 (<= Var Var)						
					 (= Var Var)						
					 (and StartBool StartBool)			
					 (or  StartBool StartBool)				
					 (not StartBool)))))

(constraint (= (next 21 UNSHEL 2 1 100 20 UNACK ) 0))
(constraint (= (next 22 c_SHEL 2 1 100 20 RTN_UNACK ) 1))

(check-synth)
