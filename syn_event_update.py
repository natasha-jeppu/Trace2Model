#######################################################################
# Generate predicates for data update across transitions
# Author: Natasha Yogananda Jeppu, natasha.yogananda.jeppu@cs.ox.ac.uk
#         University of Oxford
#######################################################################


import numpy as np
import subprocess
import time
import argparse

from os.path import abspath
from termcolor import colored

def pre_process(trace,trace_dict):

	event_types = trace_dict['event_types']
	update_var = trace_dict['update_var']
	trace_set = dict.fromkeys([i[0] for i in trace],0)

	for j in range(len(trace)-1):
		temp1 = trace[j][1:]
		update_ind = event_types[trace[j+1][0]][0].index(update_var) + 1
		temp1.append(trace[j+1][update_ind])
		if(trace_set[trace[j][0]] == 0):
			trace_set[trace[j][0]] = [temp1]
		else:
			trace_set[trace[j][0]].append(temp1)

	input_dict = {'trace_set': trace_set}

	return input_dict

def syn_int_file(input_syn,j):
	temp = input_syn['input']
	data_type = input_syn['data_type']
	value = input_syn['value']
	window = input_syn['window']

	last_ind = len(temp[0]) - 1

	f = open(full_path + 'aux_files/gen_event_update.sl','w')
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
	f.write("\
				 (+ Start Start)						\n\
				 (- Start Start)						\n\
				 (* Start Start)\n")

	num_data = [x for x in data_type if x[1] == 'N']
	for k in range(len(num_data)):
		f.write("				 " + num_data[k][0] + "\n")

	for x in value:
		f.write("				 " + str(x) + "\n")

	f.write("				 (ite StartBool Start Start)")
	f.write("))\n\n")


	f.write("	 (StartBool Bool (\n")
	bool_data = [x for x in data_type if x[1] == 'S']
	for k in range(len(bool_data)):
		f.write("				 	 " + bool_data[k][0] + "\n")

	f.write("\
					 (>= Start Start)						\n\
					 (<= Start Start)						\n\
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
	while(count < window):
		if(j+count == len(temp)):
			break;
		f.write("(constraint (= (next ")
		for x in range(last_ind):
			if(data_type[x][1] == 'N'):
				f.write(str(round(float(temp[j+count][x]))) + " ")
			elif(data_type[x][1] == 'S'):
				if (temp[j+count][x] == 'true'):
					f.write("true ")
				else:
					f.write("false ")

		f.write(") " + str(round(float(temp[j+count][last_ind]))) + "))\n")

		count = count + 1
			 
	f.write("\n(check-synth)\n")

	f.close()


def syn_bool_file(input_syn,j):
	temp = input_syn['input']
	data_type = input_syn['data_type']
	value = input_syn['value']
	window = input_syn['window']

	last_ind = len(temp[0]) - 1

	f = open(full_path + 'aux_files/gen_event_update.sl','w')
	f.write("(set-logic LIA)\n")
	f.write("(synth-fun next (")

	for x in data_type:
		f.write("(" + x[0] + " ")
		if(x[1] == 'N'):
			f.write("Int) ")
		elif(x[1] == 'S'):
			f.write("Bool) ")

	f.write(") Bool\n")

	f.write("	((Start Bool (\n")
	f.write("				 true\n")
	f.write("				 false\n")
	bool_data = [x for x in data_type if x[1] == 'S']
	for k in range(len(bool_data)):
		f.write("			 	 " + bool_data[k][0] + "\n")

	f.write("\
				 (>= Start_Int Start_Int)						\n\
				 (<= Start_Int Start_Int)						\n\
				 (and Start Start)			\n\
				 (or  Start Start)				\n\
				 (not Start)")
	f.write("))\n\n")


	f.write("	 (Start_Int Int (\n")
	f.write("\
					(+ Start_Int Start_Int)						\n\
					(- Start_Int Start_Int)						\n\
					(* Start_Int Start_Int)\n")

	num_data = [x for x in data_type if x[1] == 'N']
	for k in range(len(num_data)):
		f.write("					" + num_data[k][0] + "\n")

	for x in value:
		f.write("					" + str(x) + "\n")

	f.write("					(ite Start Start_Int Start_Int)")


	
	f.write("))))\n\n")


			
	for x in data_type:
		if(x[1] == 'N'):
			f.write("(declare-var " + x[0] + " Int)\n")
		elif(x[1] == 'S'):
			f.write("(declare-var " + x[0] + " Bool)\n")

	f.write("\n\n")

	count = 0
	while(count < window):
		if(j+count == len(temp)):
			break;
		f.write("(constraint (= (next ")
		for x in range(last_ind):
			if(data_type[x][1] == 'N'):
				f.write(str(round(float(temp[j+count][x]))) + " ")
			elif(data_type[x][1] == 'S'):
				f.write(str(temp[j+count][x]) + ' ')

		f.write(") " + str(temp[j+count][last_ind]) + "))\n")

		count = count + 1
			 
	f.write("\n(check-synth)\n")

	f.close()

def gen_syn(input_dict,trace_dict):
	trace_set = input_dict['trace_set']
	event_types = trace_dict['event_types']
	event_keys = trace_dict['event_keys']
	update_var = trace_dict['update_var']
	synth_tool = trace_dict['synth_tool']
	const_grammar = trace_dict['const_grammar']
	window = trace_dict['window']

	trace_events = dict.fromkeys(event_types.keys(),0)


	for i in trace_set.keys():
		event = []
		temp = trace_set[i]

		if(temp == 0):
			continue

		last_ind = len(temp[0]) - 1
		value = [0,1]

		print(i)
		print(event_types[i])

		next_event = np.unique([x[last_ind] for x in temp])
		data_type = [x.split(':') for x in event_types[i][0]]

		for x in const_grammar:
			value.append(x)
		
		value = np.unique(value)

		if(len(next_event) == 0):
			continue
		

		if(len(event_keys) != 1):
			window = len(temp)

		
		input_syn = {'input':temp, 'data_type':data_type, 'value':value, 'window':window}

		j=0

		while((j+window) <= len(temp)):
			if(update_var.split(':')[1] == 'N'):
				syn_int_file(input_syn,j)
				j=j+1
			elif(update_var.split(':')[1] == 'S'):
				syn_bool_file(input_syn,j)
				j=j+1

			if(synth_tool == 'cvc4'):
				p = subprocess.Popen('cvc4 ' + full_path + 'aux_files/gen_event_update.sl --lang sygus', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			elif(synth_tool == 'fastsynth'):
				p = subprocess.Popen('fastsynth ' + full_path + 'aux_files/gen_event_update.sl', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


			try:
				output, o_err = p.communicate(timeout = 5)
				if(synth_tool == 'fastsynth'):
					output = str(output).split('\\n')
				p.kill()
			except subprocess.TimeoutExpired:
				p.kill()
				print(colored("[WARNING] TIMEOUT",'magenta'))
				event.append('')
				continue
			except subprocess.CalledProcessError:
				p.kill()
				print(colored("[WARNING] FAILED",'magenta'))
				event.append('')
				continue

			if(synth_tool == 'cvc4'):
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

				if(update_var.split(':')[1] == 'N'):
					op_reg = op_reg + ') Int '
				elif(update_var.split(':')[1] == 'S'):
					op_reg = op_reg + ') Bool '

				output = output.replace(op_reg,'').replace(')\\n','')
				update_ind = event_types[i][0].index(update_var)
				event.append(data_type[update_ind][0] + '\' = ' + output)

			elif(synth_tool == 'fastsynth'):
				found = [i for i in output if('SMT: synth_fun::next -> ' in i)]
				if(not found):
					print(colored("[WARNING] FAILED",'magenta'))
					event.append('')
					continue
				expr = [i for i in output if('SMT: synth_fun::next -> ' in i)][0]
				temp_expr_simple = expr.replace('SMT: synth_fun::next -> ','')
				for x in data_type:
					temp_replace = temp_expr_simple.replace('|synth::parameter' + str(data_type.index(x)) + '|',x[0])
					temp_expr_simple = temp_replace
				update_ind = event_types[i][0].index(update_var)
				event.append(data_type[update_ind][0] + '\' = ' + temp_expr_simple)

		trace_events[i] = event
		print(colored(event,'green'))

	return trace_events




def parse_args():
	parser = argparse.ArgumentParser()
	required_parse = parser.add_argument_group('required arguments')
	required_parse.add_argument('-i','--input_file', metavar = 'INPUT_FILENAME', required=True,
            help='Input trace file for data update predicate generation')
	required_parse.add_argument('-v', '--var', metavar = 'UPDATE_VAR', required=True,
            help='Variable for data update predicate synthesis. Use \'-v help\' for possible options')
	parser.add_argument('-dv', '--dvar_list', metavar = 'EVENT_NAME DEPENDENT_VARIABLE_LIST', action='append', nargs='+', default=[],
            help='Variables that affect update variable behaviour. Use \'-dv help\' for possible options. Use -dv [all] <var_list> to set variables for all events')
	parser.add_argument('-s','--synth_tool', metavar = 'SYNTHESIS_TOOL', default='fastsynth', choices = ['cvc4','fastsynth'],
            help='Synthesis tool for predicate generation: fastsynth or cvc4')
	parser.add_argument('-c','--const', metavar = 'GRAMMAR_CONST', default=[], type=int, nargs='+',
            help='Constants to be added to grammar for SyGus CVC4')
	parser.add_argument('-w','--window', metavar = 'SLIDING_WINDOW_SIZE', default=3, type=int,
            help='Sliding window size for predicate synthesis')

	hyperparams = parser.parse_args()
	return hyperparams



def main():

	hyperparams = parse_args()
	print(hyperparams)

	trace_filename = hyperparams.input_file
	update_var = hyperparams.var
	var_list = hyperparams.dvar_list
	synth_tool = hyperparams.synth_tool
	const_grammar = hyperparams.const
	window = hyperparams.window

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


	for x in event_types:
		if(update_var not in event_types[x][0]):
			print(colored("\n[ERROR] Wrong update variable option",'red'))
			print(colored("[HELP]",'green') + " Possible options:")
			print(event_types)
			exit()

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

	if(['help'] in var_list or 'help' in update_var):
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

		var_list_ind = dict.fromkeys(event_keys,0)
		for i in var_list:
			temp = []
			temp = [event_types[i[0]][0].index(x) + 1 for x in event_types[i[0]][0] if x in i[1:]]
			temp.append(event_types[i[0]][0].index(update_var) + 1)
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


	trace_dict = {'trace_id':trace_id, 'type_id':type_id, 'event_keys':event_keys, 'event_types':event_types, 'update_var':update_var, 'synth_tool':synth_tool, 'const_grammar':const_grammar, 'window':window}

	f = open(trace_filename.replace('.txt','') + '_events.txt','w')
	f.close()

	if(len(event_keys) == 1):
		for i in range(len(trace_id) - 1):
			f = open(trace_filename.replace('.txt','') + '_events.txt','a')
			temp = []
			temp = events_split[trace_id[i]+1:trace_id[i+1]]
			print("----------- Trace: " + str(i+1) + " ------\n" )
			if(not temp):
				continue

			if(len(temp) < 2):
				f.close()
				continue

			input_dict = pre_process(temp,trace_dict)
			trace_events = gen_syn(input_dict,trace_dict)
			print(colored(trace_events,'green'))

			if(i == 0):
				f.write("start\n")
			for j in range(len(trace_events[event_keys[0]])):
				if(trace_events[event_keys[0]][j] != ''):
					f.write(trace_events[event_keys[0]][j] + '\n')

			f.write("start\n") 
			f.close()
	else:
		f = open(trace_filename.replace('.txt','') + '_events.txt','w')
		f.close()

		for i in range(len(trace_id) - 1):
			f = open(trace_filename.replace('.txt','') + '_events.txt','a')
			temp = []
			temp = events_split[trace_id[i]+1:trace_id[i+1]]
			print("----------- Trace: " + str(i+1) + " ------\n" )
			if(not temp):
				continue

			if(len(temp) < 2):
				f.write("start\n")
				f.write(temp[0][0] + '\n')
				f.close()
				continue

			input_dict = pre_process(temp,trace_dict)
			trace_events = gen_syn(input_dict,trace_dict)
			print(colored(trace_events,'green'))

			if(i == 0):
				f.write("start\n")
			for j in range(0,len(temp)-1):
				if(trace_events[temp[j][0]][0] == ''):
					f.write(temp[j][0] + '\n')
				else:
					f.write(temp[j][0] + ', ' + trace_events[temp[j][0]][0] + '\n')
			f.write(temp[j+1][0] + '\n')

			f.write("start\n") 
			f.close()

full_path = abspath(__file__).replace('syn_event_update.py','')
if __name__ == '__main__':
	start_time = time.time()
	main()
	end_time = time.time()
	print('\n\nTime taken: ' + str(end_time - start_time))


