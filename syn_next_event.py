#######################################################################
# Generate transition conditions for next event
# Author: Natasha Yogananda Jeppu, natasha.yogananda.jeppu@cs.ox.ac.uk
#         University of Oxford
#######################################################################

import sys
import numpy as np
import subprocess
import time
import re

import statistics as stat
import argparse

from os.path import abspath
from termcolor import colored

def pre_process(trace):

	trace_set = dict.fromkeys([i[0] for i in trace],0)

	j = 0
	for j in range(len(trace)-1):
		temp1 = trace[j][1:]
		temp1.append(trace[j+1][0])
		if(trace_set[trace[j][0]] == 0):
			trace_set[trace[j][0]] = [temp1]
		else:
			trace_set[trace[j][0]].append(temp1)
	temp1 = trace[j+1][1:]
	temp1.append('-')
	if(trace_set[trace[j+1][0]] == 0):
		trace_set[trace[j+1][0]] = [temp1]
	else:
		trace_set[trace[j+1][0]].append(temp1)

	input_dict = {'trace_set': trace_set}

	return input_dict

def simplify(expression,data_type):
	print("\nInitial expr: ")
	print(expression)

	expr_split = expression.split(' and ')

	expr_simple = ''
	list_mult_cond = []
	for x in data_type:
		list_cond = [y for y in expr_split if x[0] in y and not (any(z[0] in y for z in data_type if z!=x))]

		for y in expr_split:
			if(x[0] in y and y not in list_cond and y not in list_mult_cond):
				list_mult_cond.append(y)

		if(list_cond):
			print("Variable: " + x[0])
			f = open(full_path + 'aux_files/simplify_event.sl','w')
			f.write('(set-logic LIA)\n')
			f.write('(synth-fun inv ((' + x[0])
			if(x[1] == 'N'):
				f.write(' Int)) Bool)\n')
			elif(x[1] == 'S'):
				f.write(' Bool)) Bool)\n')

			f.write('\n(declare-var ' + x[0])
			if(x[1] == 'N'):
				f.write(' Int)\n')
			elif(x[1] == 'S'):
				f.write(' Bool)\n')

			f.write('\n(constraint (= (inv ' + x[0] +') ')
			if (len(list_cond) == 1):
				i = 0
				if ('!' in list_cond[i]):
					f.write('(not ' + list_cond[i].replace('!', '') + ')))')
				else:
					f.write(list_cond[i] + '))')
			else:
				i = 0
				for i in range(len(list_cond)-1):
					if('!' in list_cond[i]):
						f.write('(and (not ' + list_cond[i].replace('!','') + ')')
					else:
						f.write('(and ' + list_cond[i])

				i = i + 1
				if('!' in list_cond[i]):
					f.write('(not ' + list_cond[i].replace('!','') + ')')
				else:
					f.write(' ' + list_cond[i])
				for j in range(i+2):
					f.write(')')
			f.write('\n\n')
			f.write('(check-synth)')
			f.close()

			p = subprocess.Popen('fastsynth ' + full_path + 'aux_files/simplify_event.sl', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

			try:
				output, o_err = p.communicate(timeout=10)
				output = str(output).split('\\n')
				p.kill()
			except subprocess.CalledProcessError:
				p.kill()
				print(colored("[WARNING] FAILED",'magenta'))
				temp_expr_simple = ' and '.join(list_cond)

				if(expr_simple == ''):
					expr_simple = temp_expr_simple
				elif(temp_expr_simple != ''):
					expr_simple = expr_simple + ' and ' + temp_expr_simple
				continue
			except subprocess.TimeoutExpired:
				p.kill()
				print(colored("[WARNING] TIMEOUT",'magenta'))
				temp_expr_simple = ' and '.join(list_cond)

				if(expr_simple == ''):
					expr_simple = temp_expr_simple
				elif(temp_expr_simple != ''):
					expr_simple = expr_simple + ' and ' + temp_expr_simple
				continue

			expr = [i for i in output if('SMT: synth_fun::inv -> ' in i)][0]
			temp_expr_simple = expr.replace('SMT: synth_fun::inv -> ','').replace('|synth::parameter0|',x[0])

			if('(ite' in temp_expr_simple):
				temp_expr_simple = ' and '.join(list_cond)

			if(expr_simple == ''):
				expr_simple = temp_expr_simple
			elif(temp_expr_simple != ''):
				expr_simple = expr_simple + ' and ' + temp_expr_simple

	for x in list_mult_cond:
		expr_simple = expr_simple + ' and ' + x

	return(expr_simple)



def post_process(output,next_event,data_type,trace_dict):
	event_keys = trace_dict['event_keys']
	output_split = output.split()
	syn_event = dict.fromkeys([event_keys[x] for x in next_event],0)

	for i in range(len(output_split)-1,-1,-1):
		if (output_split[i] in ['(+','(-','(*','(<=','(>=']):
			output_split[i : i+3] = [''.join(x + ' ' for x in output_split[i:i+3])]


	cond = []
	arg1 = []
	arg2 = []

	for i in range(len(output_split)-1,-1,-1):
		if (output_split[i] == '(ite'):
			cond.append(output_split[i+1])
			arg1.append(output_split[i+2])
			arg2.append(output_split[i+3])
			output_split[i : i+4] = [''.join(x + ' ' for x in output_split[i:i+4])]


	print("Conditions: ")
	print(cond)
	print("Arg1: ")
	print(arg1)
	print("Arg2: ")
	print(arg2)

	e_char = [x for x in arg1 if ('(ite' not in x)]

	for x in arg2:
		if ('(ite' not in x):
			e_char.append(x)

	e_int = np.unique([int(re.search('[0-9]+',x).group(0)) for x in e_char])
	print("next_event: ")
	print(e_int)

	for j in e_int:
		char_list = [x for x in e_char if (str(j) in x)]

		temp = []
		cond_list = []

		for i in range(len(cond)):

			arg1_temp = arg1[i]
			arg2_temp = arg2[i]
			for x in cond:
				arg1_temp = arg1_temp.replace(x,'')
				arg2_temp = arg2_temp.replace(x,'')

			if ('(ite' in arg1_temp):
				c1 = any((' ' + x + ' ') in arg1_temp for x in char_list)
			else:
				c1 = any(x in arg1_temp for x in char_list)

			if ('(ite' in arg2_temp):
				c2 = any((' ' + x + ' ') in arg2_temp for x in char_list)
			else:
				c2 = any(x in arg2_temp for x in char_list)

			if(c1):
				if(cond[i] not in cond_list):
					cond_list.append(cond[i].strip())
				found = 0
				for x in cond_list:
					if(x in arg1[i]):
						found = 1
						for ind in [temp.index(y) for y in temp if x in y and cond[i].strip() not in y]:
							temp[ind] = temp[ind] + ' and ' + cond[i].strip()
				if(not found):
					temp.append(cond[i].strip())

			if(c2):
				if(cond[i] not in cond_list):
					cond_list.append(cond[i].strip())
				found = 0
				for x in cond_list:
					if(x in arg2[i]):
						found = 1
						for ind in [temp.index(y) for y in temp if x in y and cond[i].strip() not in y]:
							temp[ind] = temp[ind] + ' and !' + cond[i].strip()
				if(not found):
					temp.append('!' + cond[i].strip())

		for i in range(len(temp)):
			temp[i] = simplify(temp[i],data_type)
			print(colored('Final expr: ','green'))
			print(colored(temp[i],'green'))

		syn_event[event_keys[j]] = '(' + temp[0] + ')'
		for i in range(1,len(temp)):
			syn_event[event_keys[j]] = syn_event[event_keys[j]] + ' or (' + temp[i] + ')'


	return syn_event



def gen_syn(input_dict,trace_dict):

	trace_set = input_dict['trace_set']
	event_types = trace_dict['event_types']
	event_keys = trace_dict['event_keys']
	const_grammar = trace_dict['const_grammar']

	trace_events = dict.fromkeys(event_types.keys(),0)

	for i in trace_set.keys():
		event = 0
		temp = trace_set[i]

		last_ind = len(temp[0]) - 1
		value = [1,2]

		print('---------------' + i + '----------------')
		print(event_types[i])

		next_event = np.unique([event_keys.index(x[last_ind]) for x in temp if x[last_ind] != '-'])
		data_type = [x.split(':') for x in event_types[i][0]]

		if(const_grammar):
			for x in const_grammar:
				value.append(x)
		else:
			for x in range(last_ind):
				if(data_type[x][1] == 'N'):
					data = [round(float(y[x])) for y in temp]
					if(len(data) > 1):
						value.append(int(round(stat.stdev([round(float(y[x])) for y in temp]))))
					value.append(int(round(np.mean([round(float(y[x])) for y in temp]))))

		value = np.unique(value)

		if(len(next_event) == 0):
			continue

		j=0
		while(j < len(temp)):
			f = open(full_path + 'aux_files/gen_event.sl','w')
			f.write("(set-logic LIA)\n")
			f.write("(synth-fun next (")

			for x in data_type:
				f.write("(" + x[0] + " ")
				if(x[1] == 'N'):
					f.write("Int) ")
				elif(x[1] == 'S'):
					f.write("Bool) ")

			f.write(") Int\n")
			f.write("	((Start Int (\n")
			for k in range(len(next_event)):
				f.write("				 " + str(next_event[k]) + "\n")
			f.write("				 (ite StartBool Start Start)")
			f.write("))\n\n")

			f.write("	(Var Int (\n")
			for x in value:
				f.write("			 " + str(x) + "\n")

			num_data = [x for x in data_type if x[1] == 'N']
			for k in range(len(num_data)):
				f.write("			 " + num_data[k][0] + "\n")

			f.write("\
			 (+ Var Var)						\n\
			 (- Var Var)						\n\
			 (* Var Var)")
			f.write("))\n\n")


			f.write("	 (StartBool Bool (\n")
			bool_data = [x for x in data_type if x[1] == 'S']
			for k in range(len(bool_data)):
				f.write("				 	 " + bool_data[k][0] + "\n")

			f.write("\
					 (>= Var Var)						\n\
					 (<= Var Var)						\n\
					 (and StartBool StartBool)			\n\
					 (or  StartBool StartBool)				\n\
					 (not StartBool)")

			f.write("))))\n\n")



			for x in data_type:
				if(x[1] == 'N'):
					f.write("(declare-var " + x[0] + " Int)\n")
				elif(x[1] == 'S'):
					f.write("(declare-var " + x[0] + " Bool)\n")

			f.write("\n\n")

			count = 0
			while(count < len(temp)):
				if(j+count == len(temp)):
					break;
				if(temp[j+count][last_ind] == '-'):
					count = count + 1
					continue;
				f.write("(constraint (= (next ")
				for x in range(last_ind):
					if(data_type[x][1] == 'N'):
						f.write(str(round(float(temp[j+count][x]))) + " ")
					elif(data_type[x][1] == 'S'):
						if (temp[j+count][x] == 'true'):
							f.write("true ")
						else:
							f.write("false ")

				f.write(") " + str(event_keys.index(temp[j+count][last_ind])) + "))\n")

				count = count + 1

			j=j+count
			f.write("\n(check-synth)\n")

			f.close()

			p = subprocess.Popen('cvc4 '+ full_path + 'aux_files/gen_event.sl --lang sygus', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			try:
				output,o_err = p.communicate(timeout=5)
				p.kill()
			except subprocess.TimeoutExpired:
				p.kill()
				print(colored("[WARNING] TIMEOUT",'magenta'))
				event = 0
				continue

			output = str(output).replace('b\'unsat\\n','').replace('\'','')

			op_reg = '(define-fun next ('

			for x in data_type:
				op_reg = op_reg + '(' + x[0] + ' '
				if(x[1] == 'N'):
					op_reg = op_reg + 'Int)'
				elif(x[1] == 'S'):
					op_reg = op_reg + 'Bool)'
				if(data_type.index(x) < len(data_type) - 1):
					op_reg = op_reg + ' '

			op_reg = op_reg + ') Int '
			output = output.replace(op_reg,'').replace(')\\n','')
			event = post_process(output,next_event,data_type,trace_dict)

		trace_events[i] = event
		print(colored(event,'green'))

	return trace_events


def parse_args():
	parser = argparse.ArgumentParser()
	required_parse = parser.add_argument_group('required arguments')
	required_parse.add_argument('-i','--input_file', metavar = 'INPUT_FILENAME', required = True,
            help='Input trace file for data update predicate generation')
	parser.add_argument('-dv', '--dvar_list', metavar = 'EVENT_NAME DEPENDENT_VARIABLE_LIST', action='append', nargs='+', default=[],
            help='Variables that affect update variable behaviour')
	parser.add_argument('-c','--const', metavar = 'GRAMMAR_CONST', default=[], type=int, nargs='+',
            help='Constants to be added to grammar for SyGus CVC4')

	hyperparams = parser.parse_args()
	return hyperparams

def main():

	hyperparams = parse_args()
	print(hyperparams)

	trace_filename = hyperparams.input_file
	var_list = hyperparams.dvar_list
	const_grammar = hyperparams.const

	f = open(trace_filename,'r')
	events_raw = f.readlines()
	f.close()

	events = [x.replace('\n','') for x in events_raw]
	events_split = [x.split() for x in events]

	trace_id = [ind for ind in range(len(events_split)) if events_split[ind][0] == 'trace']
	type_id = [ind for ind in range(len(events_split)) if events_split[ind][0] == 'types']

	event_types = dict.fromkeys([events_split[ind][0] for ind in range(type_id[0]+1,trace_id[0])],0)
	event_keys = list(event_types.keys())

	for i in event_types:
		temp = []
		temp = [events_split[ind][1:] for ind in range(type_id[0]+1,trace_id[0]) if events_split[ind][0] == i]
		event_types[i] = temp

	for x in var_list:
		if(x[0] == '[all]'):
			for y in event_types:
				if(any(True for z in x[1:] if z not in event_types[y][0])):
					print(colored("\n[ERROR] Wrong dependent variable option",'red'))
					print(colored("[HELP]",'green') + " Possible options:")
					print(event_types)
					exit()
		elif(any(True for y in x[1:] if y not in event_types[x[0]][0])):
			print(colored("\n[ERROR] Wrong dependent variable option",'red'))
			print(colored("[HELP]",'green') + " Possible options:")
			print(event_types)
			exit()

	if(['help'] in var_list):
		print(colored("[HELP]",'green') + " Possible options:")
		print(event_types)
		exit()

	if(var_list):
		if(var_list[0][0] == '[all]'):
			temp_list = []
			for i in event_keys:
				temp = [i]
				for j in var_list[0][1:]:
					temp.append(j)
				temp_list.append(temp)
			var_list = temp_list

		print(var_list)
		var_list_ind = dict.fromkeys(event_keys,0)
		for i in var_list:
			temp = []
			temp = [event_types[i[0]][0].index(x) + 1 for x in event_types[i[0]][0] if x in i[1:]]
			temp = np.unique(temp)
			var_list_ind[i[0]] = [0]
			for j in temp:
				var_list_ind[i[0]].append(j)

		print(var_list_ind)

		temp = []
		for x in events_split:
			if(len(x) > 1):
				if(var_list_ind[x[0]] == 0):
					temp.append(x)
				else:
					temp.append([x[ind] for ind in var_list_ind[x[0]]])
			else:
				temp.append([x[0]])

		events_split = temp

		trace_id = [ind for ind in range(len(events_split)) if events_split[ind][0] == 'trace']
		type_id = [ind for ind in range(len(events_split)) if events_split[ind][0] == 'types']

		event_types = dict.fromkeys([events_split[ind][0] for ind in range(type_id[0]+1,trace_id[0])],0)
		event_keys = list(event_types.keys())

		for i in event_types:
			temp = []
			temp = [events_split[ind][1:] for ind in range(type_id[0]+1,trace_id[0]) if events_split[ind][0] == i]
			event_types[i] = temp

	trace_dict = {'trace_id':trace_id, 'type_id':type_id, 'event_keys':event_keys, 'event_types':event_types, 'const_grammar':const_grammar}

	f = open(trace_filename.replace('.txt','') + '_events.txt','w')
	f.close()

	for i in range(len(trace_id) - 1):
		f = open(trace_filename.replace('.txt','') + '_events.txt','a')
		temp = events_split[trace_id[i]+1:trace_id[i+1]]
		print("----------- Trace: " + str(i+1) + " ------\n" )
		if(not temp):
			continue

		if(len(temp) < 2):
			f.write("start\n")
			f.write(temp[0][0] + '\n')
			f.close()
			continue

		input_dict = pre_process(temp)
		trace_events = gen_syn(input_dict,trace_dict)
		print(colored(trace_events,'green'))

		if(i == 0):
			f.write("start\n")
		f.write(temp[0][0] + '\n')
		for j in range(1,len(temp)):
			if(trace_events[temp[j-1][0]] == 0):
				f.write(temp[j][0] + '\n')
			elif(trace_events[temp[j-1][0]][temp[j][0]] == 0):
				f.write(temp[j][0] + '\n')
			else:
				f.write(trace_events[temp[j-1][0]][temp[j][0]] + ': ' + temp[j][0] + '\n')
		f.write("start\n")
		f.close()

full_path = abspath(__file__).replace('syn_next_event.py','')
if __name__ == '__main__':
	start_time = time.time()
	main()
	end_time = time.time()
	print('\n\nTime taken: ' + str(end_time - start_time))
