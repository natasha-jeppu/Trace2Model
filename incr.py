import sys
import re
import random
import numpy as np
import os
import json
import time
import itertools

# for displaying model
from transitions import *
from transitions.extensions import GraphMachine
from pygraphviz import *

from os.path import abspath
from termcolor import colored

import argparse

def text_preprocess(start_index,hyperparams,var):

	events_tup_to_list = var['events_tup_to_list']
	o_event_uniq = var['o_event_uniq']

	len_seq = hyperparams.window

	events = events_tup_to_list[start_index]
	event_uniq = list(set(events))
	event_uniq.sort(key=events.index)

	if o_event_uniq:
		for e in event_uniq:
			if e not in o_event_uniq:
				o_event_uniq.append(e)
		event_uniq = o_event_uniq

	event_id = []

	for i in range(len(events)):
		event_id.append(event_uniq.index(events[i])+1)


	seq_input = [];
	if(len(events) < len_seq):
		seq_input = [event_id]
	for i in range(len(events)-len_seq+1):
		ind = i
		seq_input.append(event_id[ind:ind+len_seq])

	seq_input_uniq,u_ind = np.unique(seq_input,return_index=True,axis=0)
	seq_input_uniq = seq_input_uniq[np.argsort(u_ind)]

	
	print("\n\n\n******************************************** Iteration:" + str(start_index))
	print(events)

	if ((len(seq_input_uniq)*len_seq) > len(event_id)):
		print(colored('[WARNING] Using non segmented','magenta'))
		seq_input_uniq = [event_id]
	else:
		print(colored('[WARNING] Using segmented','magenta'))

	

	input_dict = {'event_id':event_id, 'seq_input_uniq':seq_input_uniq, 'event_uniq':event_uniq, 'len_seq':len_seq, 'seq_input_uniq_ce':[]}
	return input_dict


def gen_c_model(trace_input,constraint,num_states,start_index,init_model,var):

	seq_input_uniq = trace_input['seq_input_uniq']
	event_uniq = trace_input['event_uniq']
	incr = var['incr']

	f = open(C_gen_model,'w')

	data_type = {'seq' : 'uint16_t' if len(seq_input_uniq[0]) > 255 else 'uint8_t',
				 'num_seq' : 'uint16_t' if len(seq_input_uniq) > 255 else 'uint8_t',
				 'e_uniq' : 'uint16_t' if len(event_uniq) > 255 else 'uint8_t',
				 'num_states' : 'uint16_t' if num_states > 255 else 'uint8_t',
				 'init_model' : 'uint16_t' if len(init_model) > 255 else 'uint8_t',
				 'count' : 'uint16_t' if (len(seq_input_uniq[0])*len(seq_input_uniq)+len(init_model)) > 255 else 'uint8_t'}

	f.write("// ******************************************** Iteration:" + str(start_index) + "\n\n")
	f.write("#include<stdio.h>\n#include<stdbool.h>\n#include<stdint.h>\nvoid main()\n{\n\
	" + data_type['seq'] + " event_seq_length = " + str(len(seq_input_uniq[0])) + ";\n")

	f.write("	" + data_type['num_seq'] + " num_input = " + str(len(seq_input_uniq)) + ";\n")
	f.write("	" + data_type['e_uniq'] + " event_seq[" + str(len(seq_input_uniq)) + "][" + str(len(seq_input_uniq[0])) + "] = ")
	f.write("{")

	for i in range(len(seq_input_uniq)):
		f.write("{")
		for j in range(len(seq_input_uniq[0])-1):
			f.write("%d," %seq_input_uniq[i][j])
		j = j + 1
		f.write(str(seq_input_uniq[i][j]))
		if (i == len(seq_input_uniq)-1):
			f.write("}")
		else:
			f.write("},")
	f.write("};\n")

	
	f.write("	" + data_type['num_states'] + " num_states = " + str(num_states) + ";\n")
	f.write("	" + (data_type['num_states'] if num_states > len(event_uniq) else data_type['e_uniq']) + " t[" + str(len(seq_input_uniq[0])*len(seq_input_uniq)+len(init_model)) + "][3];\n")

	f.write("	" + data_type['count'] + " count=0;\n")

	if incr:
		f.write("	" + (data_type['num_states'] if num_states > len(event_uniq) else data_type['e_uniq']) + " t_gen[" + str(len(init_model)) + "][3] = ");
		f.write("{")

		for i in range(len(init_model)):
			f.write("{")
			for j in range(len(init_model[i])-1):
				f.write("%d," %init_model[i][j])
			j = j + 1
			f.write(str(init_model[i][j]))
			if (i == len(init_model)-1):
				f.write("}")
			else:
				f.write("},")
		f.write("};\n\n")

		f.write("	for(" + data_type['init_model'] + " i=0;i<" + str(len(init_model)) + ";i++)				\n\
		{																		\n\
			t[count][0] = t_gen[i][0];											\n\
			t[count][1] = t_gen[i][1];											\n\
			t[count][2] = t_gen[i][2];											\n\
			count = count + 1;													\n\
		}\n")

	f.write(" 																		\n\
	for (" + data_type['num_seq'] + " i=0;i<num_input;i++) 													\n\
	{																				\n\
		" + data_type['num_states'] + " start_state_var;														\n\
		__CPROVER_assume(start_state_var <= num_states && start_state_var > 1);		\n\
		assert(start_state_var <= num_states);										\n\n\
		t[count][0] = start_state_var;												\n\
		for (" + data_type['seq'] + " j=0;j<event_seq_length;j++)										\n\
		{																			\n\
			" + data_type['num_states'] + " next_state_var;														\n\
			t[count][1] = event_seq[i][j];											\n\
			if(event_seq[i][j] == 1)												\n\
				t[count][0] = 1;													\n\
			__CPROVER_assume(next_state_var <= num_states && next_state_var > 1);	\n\
			assert(next_state_var <= num_states);									\n\
			t[count][2] = next_state_var;											\n\
			count = count+1;															\n\
			t[count][0] = t[count-1][2];											\n\
		}																			\n\
	}\n\n")

	f.write("	bool in[num_states][" + str(len(event_uniq)) + "];												\n\
	bool o[num_states][" + str(len(event_uniq)) + "];														\n\
																					\n\
	for (" + data_type['num_states'] + " i=0;i<num_states;i++)												\n\
		for (" + data_type['e_uniq'] + " j=0;j<" + str(len(event_uniq)) + ";j++)													\n\
		{																			\n\
			in[i][j] = false;														\n\
			o[i][j] = false;														\n\
		}																			\n\
																					\n\
	for (" + data_type['count'] + " i=0;i<count;i++)													\n\
	{																				\n\
		o[t[i][0]-1][t[i][1]-1] = true;											\n\
		in[t[i][2]-1][t[i][1]-1] = true;											\n\
	}\n")

	f.write("																		\n\
	bool wrong_transition = false;														\n\
	for (" + data_type['num_states'] + " i=0; i<num_states;i++)														\n\
	{																				\n\
	")

	if not constraint:
		f.write("")
	else:
		for i in range(len(event_uniq)):
			constraint_i = [item[1] for item in constraint if item[0] == i+1]
			event_constraint = [constraint_i[ind] for ind in range(len(constraint_i)) if constraint_i[ind] > 0]
			if event_constraint:
				if i == 0:
					f.write("		if ")
				else:
					f.write("			else if ")

				f.write("(in[i][ " + str(i) + "] && (")
			
				j = -1
				for j in range(len(event_constraint)-1):
					f.write("o[i][" + str(event_constraint[j]-1) + "] || ")
				j = j + 1
				f.write("o[i][" + str(event_constraint[j]-1) + "]))\n")
				f.write("				wrong_transition = true;\n")
			
	f.write("	}\n")

	f.write("	assert(wrong_transition != false);\n")
	f.write('}')
	f.close()

def get_model(input_dict,init_model):

	found = 0
	f = open(C_gen_model_output,'r')
	out_cbmc = json.load(f)
	f.close()

	key = 'result'
	for x in out_cbmc:
		if key in x:
			result = x['result']

	key = 'status'
	
	for x in result:
		if key in x:
			if x[key] == "FAILURE":
				failed_out = x
				found = 1

	if not found:
		return(0,[])

	t = np.zeros(((len(input_dict['seq_input_uniq'][0])*len(input_dict['seq_input_uniq'])+len(init_model)),3),dtype=int)
	if (found):
		key = 'lhs'
		key2 = 'data'

		for x in failed_out['trace']:
			if (key in x) and (key2 in x['value']):
				if (re.search('t\[.*',x[key])):
					ind = re.findall('[0-9]+',x[key])
					# print(ind)
					t[int(ind[0])][int(ind[1])] = int(x['value']['data'])
	
	t = np.unique(t,axis=0)
	t=[list(y) for y in t]
	return (found,t)


def get_ce(trace_input,var,init_model):

	events_tup_to_list = var['events_tup_to_list']

	events_uniq_full = [j for i in events_tup_to_list for j in i]
	event_uniq = list(set(events_uniq_full))
	event_uniq.sort(key=events_uniq_full.index)

	event_id = []

	for i in range(len(events_uniq_full)):
		event_id.append(event_uniq.index(events_uniq_full[i])+1)

	len_seq = 2

	seq_input = [];
	for i in range(len(event_id)-len_seq+1):
		ind = i
		seq_input.append(event_id[ind:ind+len_seq])


	seq_input_uniq = [list(i) for i in (np.unique(seq_input,axis=0))]


	event_uniq_current_trace = []


	for i in range(len(trace_input['event_uniq'])):
		event_uniq_current_trace.append(event_uniq.index(trace_input['event_uniq'][i])+1)

	a = [x[1] for x in init_model]
	a_uniq = list(set(a))

	for i in range(len(a_uniq)):
		event_uniq_current_trace.append(a_uniq[i]+1)

	event_uniq_current_trace = np.unique(event_uniq_current_trace)

	b = [list(i) for i in (itertools.product(range(1,len(event_uniq_current_trace)+1), repeat = len_seq))]
	
	not_in_seq = [b[i] for i in range(len(b)) if (b[i] not in seq_input_uniq)]

	found = 1
	if not not_in_seq:
		found = 0

	return (found,not_in_seq)

def plot_model(model,trace_input,num_states,hyperparams):
	
	trace_filename = hyperparams.input_file
	target_model_path = hyperparams.target
	order = hyperparams.order

	class vis_trace(object):
		def show_graph(self, **kwargs):
			name = trace_filename.replace('.txt','') + '_incr_' + order + '.png'
			self.get_graph().draw(name, prog='dot')
			os.system('mv ' + name + ' ' + target_model_path)
        	

	event_uniq = trace_input['event_uniq']
	event_id = trace_input['event_id']

	t = np.unique(model,axis=0)
	first_event = [ind for ind in range(len(model)) if model[ind][1] == event_id[0]]
	start_state = str(model[first_event[0]][0])
	states = []
	for i in range(num_states):
		states.append(str(i+1))

	transitions = []
	for i in range(len(t)):
		temp_trans = [event_uniq[t[i][1]-1],states[t[i][0]-1] ,states[t[i][2]-1]]
		transitions.append(temp_trans)

	model = vis_trace()
	machine = GraphMachine(model=model, 
                       states=states, 
                       transitions=transitions,
                       initial = '1',
                       show_auto_transitions=False,
                       title="trace_learn",
                       show_conditions=True)
	model.show_graph()

def nfa_traverse(model,trace):
	state = [1]
	for i in range(len(trace)):
		found = [x[2] for x in model if x[0] in state and x[1] == trace[i]]
		if not found:
			return (0,trace[0:i+1])
		else:
			state = found

	return (1,[])


def parse_args():
    parser = argparse.ArgumentParser()
    required_parse = parser.add_argument_group('required arguments')
    required_parse.add_argument('-i','--input_file', metavar = 'INPUT_FILENAME', required = True,
            help='Input trace file for data update predicate generation')
    parser.add_argument('-w', '--window', metavar = 'SLIDING_WINDOW', default=3, type=int,
            help='Sliding window size')
    parser.add_argument('-n','--num_states', metavar = 'NUM_STATES', default=2, type=int,
            help='Number of states')
    parser.add_argument('-t','--target', metavar = 'TARGET_PATH', default=full_path + 'models',
            help='Target model path')
    parser.add_argument('-o','--order', metavar = 'TRACE_ORDER', default='same', choices=['bts','stb','random','same'],
            help='Trace order')

    hyperparams = parser.parse_args()
    return hyperparams


def main():
	hyperparams = parse_args()
	# print(hyperparams)

	trace_filename = hyperparams.input_file
	num_states = hyperparams.num_states
	len_seq = hyperparams.window
	target_model_path = hyperparams.target
	order = hyperparams.order

	o_event_uniq = []
	o_event_id = []
	init_model = []
	start_state = 1


	f = open(trace_filename,'r')
	events_raw = f.readlines()
	full_events = [x.replace('\n','') for x in events_raw]
	start_id = [i for i in range(len(full_events)) if full_events[i]=='start']
	f.close()

	events_list = []
	for i in range(len(start_id)-1):
		events_list.append(full_events[start_id[i]:start_id[i+1]])


	events_tuple = list(set(tuple(x) for x in events_list))
	events_tup_to_list = [list(x) for x in events_tuple]

	if(order == 'same'):
		events_tup_to_list.sort(key=events_list.index)
	elif(order == 'bts'):
		events_tup_to_list.sort(key=len,reverse=True)
	elif(order == 'stb'):
		events_tup_to_list.sort(key=len)
	elif(order == 'random'):
		random.shuffle(events_tup_to_list)

	print(len(events_tup_to_list))

	length = [len(x) for x in events_tup_to_list]
	print("Total size:" + str(sum(length)))

	#Generate initial model

	var = {'incr': 0, 'events_tup_to_list': events_tup_to_list, 'o_event_uniq': o_event_uniq, 'o_event_id': o_event_id}

	start_index = 0

	input_dict = text_preprocess(start_index,hyperparams,var)

	ce_global = []
	found_ce = 0

	print("Finding CE")
	(found_ce,ce_global) = get_ce(input_dict,var,init_model)
	
	if found_ce:
		print("CE found :")
		print(list(ce_global))
	else:
		print("No CE found, generating model")


	while(True):
		found_model = 0

		gen_c_model(input_dict,ce_global,num_states,start_index,init_model,var)
		print("Running CBMC...............")
		os.system("cbmc " + C_gen_model + " --trace --json-ui > " + C_gen_model_output)

		(found_model,temp_model) = get_model(input_dict,init_model)

		if found_model:
			print(colored("Final Generated model",'green'))
			print(colored(temp_model,'green'))
			final_model_gen = temp_model
			break;
		else:
			num_states = num_states + 1
			print("No model, increasing number of states to %d" %(num_states))



	##Display model
	plot_model(final_model_gen,input_dict,num_states,hyperparams)


	#Increment

	init_model = final_model_gen

	while(True):

		var['incr'] = 1
		
		var['o_event_uniq'] = input_dict['event_uniq']
		var['o_event_id'] = input_dict['seq_input_uniq_ce']
		init_model = final_model_gen
		start_index = start_index + 1

		if(start_index == len(events_tup_to_list)):
			break

		input_dict = text_preprocess(start_index,hyperparams,var)

		(f,trace) = nfa_traverse(init_model,input_dict['event_id'])
		if(f):
			input_dict['seq_input_uniq_ce'] = var['o_event_id']
			continue

		print("Generating model with " + str(num_states) + " states")

		o_num_states = num_states

		
		print("Finding CE")
		(found_ce,ce_global) = get_ce(input_dict,var,init_model)
	
		if found_ce:
			print("CE found :")
			print(list(ce_global))
		else:
			print("No CE found, generating model")

		while(True):

			found_model = 0

			gen_c_model(input_dict,ce_global,num_states,start_index,init_model,var)
			print("Running CBMC...............")
			os.system("cbmc " + C_gen_model + " --trace --json-ui > " + C_gen_model_output)

			(found_model,temp_model) = get_model(input_dict,init_model)

			if found_model:
				print(colored("Final Generated model",'green'))
				print(colored(temp_model,'green'))
				final_model_gen = temp_model
				break;
			else:
				num_states = num_states + 1
				print("No model, increasing number of states to %d" %(num_states))

		##Display model
		plot_model(final_model_gen,input_dict,num_states,hyperparams)

	print("\n\n\n------------- Verifying: ----------------------------")

	start_index = -1

	while(True):

		start_index = start_index + 1

		if(start_index == len(events_tup_to_list)):
			print(colored("\nAll behaviors present",'green'))
			print(colored("Number of states: " + str(num_states),'green'))
			break

		input_dict = text_preprocess(start_index,hyperparams,var)

		(f,trace) = nfa_traverse(init_model,input_dict['event_id'])

		if(not f):
			print(colored("\n[ERROR] Missing behavior",'red'))
			print(colored(trace,'red'))
			print('\n')

			while(True):

				found_model = 0

				init_model = final_model_gen

				input_dict['seq_input_uniq'] = [trace]

				gen_c_model(input_dict,ce_global,num_states,start_index,init_model,var)
				print("Running CBMC...............")
				os.system("cbmc " + C_gen_model + " --trace --json-ui > " + C_gen_model_output)

				(found_model,temp_model) = get_model(input_dict,init_model)

				if found_model:
					print(colored("Final Generated model",'green'))
					print(colored(temp_model,'green'))
					final_model_gen = temp_model
					break;
				else:
					num_states = num_states + 1
					print("No model, increasing number of states to %d" %(num_states))

			start_index = start_index - 1
	

full_path = abspath(__file__).replace('incr.py','')
C_gen_model = full_path + 'aux_files/gen_model_v9.c'
C_gen_model_output = full_path + 'aux_files/cbmc_output_gen_model_v9.json'

if __name__ == '__main__':
	start_time = time.time()
	main()
	end_time = time.time()
	print('\n\nTime taken: ' + str(end_time - start_time))
