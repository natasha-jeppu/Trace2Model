(set-logic LIA)
(declare-datatypes ((inp.cmd_t 0))
	(((ADD) (NO_CMD) (REMOVE) (RESET) (UNSHEL) (UNSUPR) (c_ACK) (c_SHEL) (c_SUPR) )))
(declare-datatypes ((prev_out.prev_s_t 0))
	(((NORMAL) (OOS) (RTN_UNACK) (UNACK) (s_ACK) (s_SHEL) (s_SUPR) )))
(synth-fun next ((inp.val Int) (inp.cmd inp.cmd_t)(out.snooze_timer Int) (snooze_timeout Int) (high_thresh Int) (low_thresh Int) (prev_out.prev_s prev_out.prev_s_t)) Int
	((Start Int)  (Var Int) (EnumVar0 inp.cmd_t) (EnumVar1 prev_out.prev_s_t) (StartBool Bool))
	((Start Int (
				 0
				 1
				 (ite StartBool Start Start)))

	(Var Int (
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
ADD
NO_CMD
REMOVE
RESET
UNSHEL
UNSUPR
c_ACK
c_SHEL
c_SUPR
))

(EnumVar1 prev_out.prev_s_t (
	prev_out.prev_s
NORMAL
OOS
RTN_UNACK
UNACK
s_ACK
s_SHEL
s_SUPR
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

(constraint (= (next (- 1879048170) NO_CMD 0 1 100 20 NORMAL ) 0))
(constraint (= (next (- 2147483370) UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next (- 2147483546) REMOVE 1 1 100 20 s_ACK ) 0))
(constraint (= (next (- 2147483546) UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next (- 2147483546) UNSUPR 1 1 100 20 RTN_UNACK ) 0))
(constraint (= (next (- 2147483546) UNSUPR 1 1 100 20 UNACK ) 0))
(constraint (= (next (- 2147483546) c_SUPR 0 1 100 20 UNACK ) 0))
(constraint (= (next (- 2147483614) REMOVE 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next (- 2147483614) UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next (- 2147483627) UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next (- 2147483627) UNSUPR 1 1 100 20 UNACK ) 0))
(constraint (= (next (- 2147483628) UNSUPR 0 1 100 20 UNACK ) 0))
(constraint (= (next 0 NO_CMD 0 1 100 20 UNACK ) 0))
(constraint (= (next 0 NO_CMD 0 1 100 20 s_ACK ) 0))
(constraint (= (next 0 c_SHEL 0 1 100 20 s_ACK ) 0))
(constraint (= (next 100 REMOVE 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 100 UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next 100 UNSUPR 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 100 UNSUPR 0 1 100 20 UNACK ) 0))
(constraint (= (next 100 UNSUPR 0 1 100 20 s_ACK ) 1))
(constraint (= (next 100 UNSUPR 1 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 100 c_ACK 0 1 100 20 UNACK ) 0))
(constraint (= (next 100 c_SUPR 0 1 100 20 s_ACK ) 0))
(constraint (= (next 20 REMOVE 0 1 100 20 NORMAL ) 0))
(constraint (= (next 20 REMOVE 0 1 100 20 UNACK ) 0))
(constraint (= (next 20 RESET 0 1 100 20 UNACK ) 0))
(constraint (= (next 20 UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next 20 UNSUPR 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 20 UNSUPR 0 1 100 20 UNACK ) 0))
(constraint (= (next 20 UNSUPR 0 1 100 20 s_ACK ) 1))
(constraint (= (next 20 c_SHEL 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 20 c_SHEL 0 1 100 20 s_ACK ) 0))
(constraint (= (next 20 c_SUPR 0 1 100 20 s_ACK ) 0))
(constraint (= (next 21 NO_CMD 0 1 100 20 NORMAL ) 0))
(constraint (= (next 21 NO_CMD 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 21 NO_CMD 0 1 100 20 s_ACK ) 0))
(constraint (= (next 21 NO_CMD 1 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 21 REMOVE 0 1 100 20 s_ACK ) 0))
(constraint (= (next 21 RESET 0 1 100 20 s_ACK ) 0))
(constraint (= (next 21 UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next 21 UNSUPR 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 21 UNSUPR 0 1 100 20 UNACK ) 0))
(constraint (= (next 21 UNSUPR 0 1 100 20 s_ACK ) 1))
(constraint (= (next 21 UNSUPR 1 1 100 20 NORMAL ) 0))
(constraint (= (next 21 UNSUPR 1 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 21 UNSUPR 1 1 100 20 UNACK ) 0))
(constraint (= (next 21 UNSUPR 1 1 100 20 s_ACK ) 1))
(constraint (= (next 21 c_ACK 0 1 100 20 UNACK ) 0))
(constraint (= (next 21 c_SHEL 0 1 100 20 UNACK ) 0))
(constraint (= (next 21 c_SHEL 0 1 100 20 s_ACK ) 0))
(constraint (= (next 21 c_SUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next 21 c_SUPR 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 21 c_SUPR 0 1 100 20 s_ACK ) 0))
(constraint (= (next 21 c_SUPR 1 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 22 UNSUPR 0 1 100 20 NORMAL ) 0))
(constraint (= (next 23 ADD 0 1 100 20 s_ACK ) 0))
(constraint (= (next 23 UNSUPR 1 1 100 20 s_ACK ) 1))
(constraint (= (next 268435476 NO_CMD 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 268435476 c_SUPR 0 1 100 20 s_ACK ) 0))
(constraint (= (next 32 UNSUPR 0 1 100 20 UNACK ) 0))
(constraint (= (next 34 NO_CMD 0 1 100 20 s_ACK ) 0))
(constraint (= (next 34 c_SHEL 0 1 100 20 s_ACK ) 0))
(constraint (= (next 36 UNSUPR 1 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 38 UNSUPR 0 1 100 20 RTN_UNACK ) 0))
(constraint (= (next 38 c_ACK 0 1 100 20 NORMAL ) 0))

(check-synth)
