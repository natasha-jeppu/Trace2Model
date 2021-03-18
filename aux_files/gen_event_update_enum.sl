(set-logic LIA)
(declare-datatypes ((inp.cmd_t 0))
	(((inp.cmdADD) (inp.cmdNO_CMD) (inp.cmdUNSHEL) (inp.cmdc_ACK) (inp.cmdc_SHEL) (inp.cmdc_SUPR))))
(declare-datatypes ((prev_out.prev_s_t 0))
	(((prev_out.prev_sNORMAL) (prev_out.prev_sRTN_UNACK) (prev_out.prev_sUNACK) (prev_out.prev_ss_ACK))))

(synth-fun next ((inp.val Int) (inp.cmd inp.cmd_t) (out.snooze_timer Int) (snooze_timeout Int) (high_thresh Int) (low_thresh Int) (prev_out.prev_s prev_out.prev_s_t)) Int

	((Start Int) (StartBool Bool) (EnumVar0 inp.cmd_t) (EnumVar1 prev_out.prev_s_t))

	((Start Int (
		inp.val
		out.snooze_timer
		snooze_timeout
		high_thresh
		low_thresh
		1
		(+ Start Start)						
		(- Start Start)						
		(* Start Start)
		(ite StartBool Start Start)))

	 (StartBool Bool (
	 	(= EnumVar0 EnumVar0)
	 	(= EnumVar1 EnumVar1)
		(> Start Start)						
		(>= Start Start)						
		(< Start Start)						
		(<= Start Start)						
		(= Start Start)						
		(and StartBool StartBool)			
		(or  StartBool StartBool)				
		(not StartBool)))

	(EnumVar0 inp.cmd_t (
		inp.cmd
		inp.cmdADD
		inp.cmdNO_CMD
		inp.cmdUNSHEL
		inp.cmdc_ACK
		inp.cmdc_SHEL
		inp.cmdc_SUPR))

	(EnumVar1 prev_out.prev_s_t (
		prev_out.prev_s
		prev_out.prev_sNORMAL
		prev_out.prev_sRTN_UNACK
		prev_out.prev_sUNACK
		prev_out.prev_ss_ACK))

))

(constraint (= (next 102 inp.cmdNO_CMD 2 1 100 20 prev_out.prev_sRTN_UNACK ) 2))
(constraint (= (next 102 inp.cmdNO_CMD 2 1 100 20 prev_out.prev_sRTN_UNACK ) 2))
(constraint (= (next 102 inp.cmdNO_CMD 2 1 100 20 prev_out.prev_sRTN_UNACK ) 2))
(constraint (= (next 102 inp.cmdNO_CMD 2 1 100 20 prev_out.prev_sRTN_UNACK ) 2))

(check-synth)
