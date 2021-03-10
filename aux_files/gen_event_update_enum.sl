(set-logic LIA)

(declare-datatypes ((s1_t 0))
	(((s1off) (s1on) )))
(declare-datatypes ((s2_t 0))
	(((s2off) (s2on) )))
(declare-datatypes ((s3_t 0))
	(((s3off) (s3on) )))
(declare-datatypes ((s4_t 0))
	(((s4off) (s4on) )))
(declare-datatypes ((s5_t 0))
	(((s5off) (s5on) )))
(declare-datatypes ((s6_t 0))
	(((s6off) (s6on) )))
(declare-datatypes ((s7_t 0))
	(((s7off) (s7on) )))
(declare-datatypes ((s8_t 0))
	(((s8off) (s8on) )))
(declare-datatypes ((s9_t 0))
	(((s9off) (s9on) )))
(declare-datatypes ((s10_t 0))
	(((s10off) (s10on) )))
(declare-datatypes ((s11_t 0))
	(((s11off) (s11on) )))

(synth-fun next ((s1 s1_t)(s2 s2_t)(s3 s3_t)(s4 s4_t)(s5 s5_t)(s6 s6_t)(s7 s7_t)(s8 s8_t)(s9 s9_t)(s10 s10_t)(s11 s11_t)) s11_t
	((Start s11_t) (EnumVar0 s1_t) (EnumVar1 s2_t) (EnumVar2 s3_t) (EnumVar3 s4_t) (EnumVar4 s5_t) (EnumVar5 s6_t) (EnumVar6 s7_t) (EnumVar7 s8_t) (EnumVar8 s9_t) (EnumVar9 s10_t) (StartBool Bool) (Start_Int Int))
	((Start s11_t (
				s11
				s11off
				s11on
				(ite StartBool Start Start)))

	(EnumVar0 s1_t (
				s1
				s1off
				s1on
				(ite StartBool EnumVar0 EnumVar0)))

	(EnumVar1 s2_t (
				s2
				s2off
				s2on
				(ite StartBool EnumVar1 EnumVar1)))

	(EnumVar2 s3_t (
				s3
				s3off
				s3on
				(ite StartBool EnumVar2 EnumVar2)))

	(EnumVar3 s4_t (
				s4
				s4off
				s4on
				(ite StartBool EnumVar3 EnumVar3)))

	(EnumVar4 s5_t (
				s5
				s5off
				s5on
				(ite StartBool EnumVar4 EnumVar4)))

	(EnumVar5 s6_t (
				s6
				s6off
				s6on
				(ite StartBool EnumVar5 EnumVar5)))

	(EnumVar6 s7_t (
				s7
				s7off
				s7on
				(ite StartBool EnumVar6 EnumVar6)))

	(EnumVar7 s8_t (
				s8
				s8off
				s8on
				(ite StartBool EnumVar7 EnumVar7)))

	(EnumVar8 s9_t (
				s9
				s9off
				s9on
				(ite StartBool EnumVar8 EnumVar8)))

	(EnumVar9 s10_t (
				s10
				s10off
				s10on
				(ite StartBool EnumVar9 EnumVar9)))

	(StartBool Bool (
				true
				false
				(= Start Start)
	 			(= EnumVar0 EnumVar0)
	 			(= EnumVar1 EnumVar1)
	 			(= EnumVar2 EnumVar2)
	 			(= EnumVar3 EnumVar3)
	 			(= EnumVar4 EnumVar4)
	 			(= EnumVar5 EnumVar5)
	 			(= EnumVar6 EnumVar6)
	 			(= EnumVar7 EnumVar7)
	 			(= EnumVar8 EnumVar8)
	 			(= EnumVar9 EnumVar9)
				(>= Start_Int Start_Int)
				(<= Start_Int Start_Int)
				(and StartBool StartBool)
				(or  StartBool StartBool)
				(not StartBool)))

	(Start_Int Int (
				(+ Start_Int Start_Int)
				(- Start_Int Start_Int)
				(* Start_Int Start_Int)
				(ite StartBool Start_Int Start_Int)))))

(declare-var s1 s1_t)
(declare-var s2 s2_t)
(declare-var s3 s3_t)
(declare-var s4 s4_t)
(declare-var s5 s5_t)
(declare-var s6 s6_t)
(declare-var s7 s7_t)
(declare-var s8 s8_t)
(declare-var s9 s9_t)
(declare-var s10 s10_t)
(declare-var s11 s11_t)


(constraint (= (next s1on s2on s3on s4on s5on s6on s7off s8on s9off s10on s11on ) s11on))
(constraint (= (next s1on s2on s3on s4on s5on s6off s7on s8off s9on s10on s11on ) s11on))
(constraint (= (next s1on s2on s3on s4on s5off s6on s7off s8on s9on s10on s11on ) s11on))

(check-synth)
