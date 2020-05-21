#### for LCRL where transitions cannot loop back to start_state, with check at the end


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

def text_preprocess():
	# process trace events into list of indices - stored into dictionary input_dict
	# input_dict = {'event_id': sequence of events 
	#				'len_seq': length of sliding window
	#				'seq_input_uniq': event sequence blocks of length = size of sliding window, input to CBMC
	#				'event_uniq': unique events in trace}

	f = open(trace_filename,'r')
	events_raw = f.readlines()
	events = [x.replace('\n','') for x in events_raw]
	event_uniq = list(set(events))
	event_uniq.sort(key=events.index)

	event_id = []

	for i in range(len(events)):
		event_id.append(event_uniq.index(events[i])+1)


	seq_input = [];
	for i in range(len(events)-len_seq+1):
		# random windows instead of a sliding window
		# ind = random.randint(0,len(events)-3) 
		ind = i
		seq_input.append(event_id[ind:ind+len_seq])

	seq_input_uniq,u_ind = np.unique(seq_input,return_index=True,axis=0)
	print(len(seq_input_uniq)*len_seq)

	if(len(seq_input_uniq)*len_seq < len(event_id)):
		seq_input_uniq = seq_input_uniq[np.argsort(u_ind)]
	else:
		seq_input_uniq = [event_id]

	print(len(event_id))
	print(event_uniq)
	
	#print(seq_input_uniq)

	input_dict = {'event_id':event_id, 'seq_input_uniq':seq_input_uniq, 'event_uniq':event_uniq}
	f.close()
	return input_dict


def gen_c_model(trace_input,constraint,num_states):
	# Generating C code used to generate behavior model

	seq_input_uniq = trace_input['seq_input_uniq']
	event_uniq = trace_input['event_uniq']
	f = open(C_gen_model,'w')

	f.write("#include<stdio.h>\n#include<stdbool.h>\n#include<stdint.h>\nvoid main()\n{\n\
	uint8_t event_seq_length = " + str(len(seq_input_uniq[0])) + ";\n")

	f.write("	uint8_t num_input = " + str(len(seq_input_uniq)) + ";\n")
	f.write("	uint8_t event_seq[" + str(len(seq_input_uniq)) + "][" + str(len(seq_input_uniq[0])) + "] = ")
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

	f.write("	uint8_t length = sizeof(event_seq)/sizeof(event_seq[0][0]);\n");
	f.write("	uint8_t num_states = " + str(num_states) + ";\n")
	f.write("	uint8_t t[num_states][" + str(len(event_uniq)) + "];\n");

	f.write("	for (uint8_t i=0;i<num_states;i++)								\n\
		for (uint8_t j=0;j<" + str(len(event_uniq)) + ";j++)												\n\
			t[i][j] = 0;\n\n")

	if incr:
		f.write("	uint8_t t_gen[" + str(len(init_model)) + "][3] = ");
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
		f.write("};\n")
		f.write("for(uint8_t i=0;i<" + str(len(init_model)) + ";i++)											\n\
			t[t_gen[i][0]-1][t_gen[i][1]-1] = t_gen[i][2];\n")

	f.write("	bool wrong_transition = false;\n")
	if not change:
		f.write(" 																		\n\
	uint8_t temp;																	\n\
																					\n\
	for (uint8_t i=0;i<num_input;i++)												\n\
	{																				\n\
																					\n\
		uint8_t state1; 															\n\
		__CPROVER_assume(state1 <= num_states && state1 > 1);						\n\
		temp = state1;																\n\
																					\n\
		for (uint8_t j=0;j<event_seq_length;j++)									\n\
		{																			\n\
			if(i==0 && j==0)														\n\
				printf(\"%d\\n\",1);												\n\
																						\n\
			uint8_t state2;														\n\
			__CPROVER_assume(state2 <= num_states && state2 > 1);					\n\
																					\n\
			if(event_seq[i][j]==1)					\n\
			{\n\
				t[0][event_seq[i][j]-1] = t[0][event_seq[i][j]-1] ? t[0][event_seq[i][j]-1] : state2;						\n\
				temp = t[0][event_seq[i][j]-1];							\n\
			}\n\
			else																	\n\
			{\n\
				t[temp-1][event_seq[i][j]-1] = t[temp-1][event_seq[i][j]-1] ? t[temp-1][event_seq[i][j]-1] : state2;		\n\
				temp = t[temp-1][event_seq[i][j]-1];									\n\
			}\n\
																					\n\
		}																			\n\
																					\n\
	}\n")

	else:
		f.write("uint8_t temp;															\n\
	uint8_t c = 0;																		\n\
	uint8_t count = " + str(no_change) + ";																	\n\
																						\n\
	for (uint8_t i=0;i<num_input;i++)												\n\
	{																				\n\
																					\n\
		uint8_t state1; 															\n\
		__CPROVER_assume(state1 <= num_states && state1 > 1);						\n\
		temp = state1;																\n\
																					\n\
		for (uint8_t j=0;j<event_seq_length;j++)									\n\
		{																			\n\
		bool p;																		\n\
																					\n\
			if(i==0 && j==0)														\n\
				printf(\"%d\\n\",1);												\n\
																					\n\
			uint8_t state2;															\n\
			__CPROVER_assume(state2 <= num_states && state2 > 1);					\n\
																					\n\
			if(event_seq[i][j]==1)													\n\
			{																		\n\
				if(t[0][event_seq[i][j]-1]!=0)										\n\
					if(p && c<count)												\n\
					{																\n\
						t[0][event_seq[i][j]-1] = state2;							\n\
						c = c+1;													\n\
					}																\n\
					else 															\n\
						t[0][event_seq[i][j]-1] = t[0][event_seq[i][j]-1];			\n\
				else 																\n\
					t[0][event_seq[i][j]-1] = state2;								\n\
				temp = t[0][event_seq[i][j]-1];										\n\
			}																		\n\
			else																	\n\
			{																		\n\
				if(t[temp-1][event_seq[i][j]-1]!=0)									\n\
					if(p && c<count)												\n\
					{																\n\
						t[temp-1][event_seq[i][j]-1] = state2;						\n\
						c = c+1;													\n\
					}																\n\
					else 															\n\
						t[temp-1][event_seq[i][j]-1] = t[temp-1][event_seq[i][j]-1];\n\
				else 																\n\
					t[temp-1][event_seq[i][j]-1] = state2;							\n\
				temp = t[temp-1][event_seq[i][j]-1];								\n\
			}																		\n\
																					\n\
		}																			\n\
																					\n\
	}\n\n\
		bool t1[num_states];														\n\
		for (uint8_t i=0;i<num_states;i++)												\n\
			t1[i] = false;																\n\
																				\n\
		for (uint8_t i=0;i<num_states;i++)								\n\
			for (uint8_t j=0;j<" + str(len(event_uniq)) + ";j++)									\n\
			{															\n\
				if(t[i][j] > 0 && t[i][j] != i+1)											\n\
					t1[t[i][j] - 1] = true;								\n\
		}\n\
																		\n\
		for (uint8_t i=1;i<num_states;i++)								\n\
			wrong_transition = wrong_transition | !t1[i];\n")

	f.write("	for (uint8_t i=0;i<num_states;i++)								\n\
		for (uint8_t j=0;j<" + str(len(event_uniq)) + ";j++)												\n\
			printf(\"%d\",t[i][j]);\n")				


	if not constraint:
		f.write("")
	else:
		f.write("	for (uint8_t i=0; i<num_states;i++)							\n\
	{\n")
		len_ce = len(constraint[0])
		for i in range(len(constraint)):
			f.write("		if(")
			for j in range(len_ce):
				for k in range(j+1):
					f.write("t[")
				f.write("i]")
				for k in range(j+1):
					f.write("[" + str(int(constraint[i][k])-1) + "]")
					if(k < j):
						f.write("-1]")
				f.write("!=0")
				if(j < len_ce-1):
					f.write(" && ")
			f.write(")\n")
			f.write("				wrong_transition = true;\n")
		f.write("	}\n")

	f.write("	assert(wrong_transition != false);\n")
	f.write('}')
	f.close()

def get_model():
	# Process CBMC output to extract generated model
	found = 0
	f = open(C_gen_model_output,'r')
	out_cbmc = json.load(f)

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

	t = []
	start_state = 0
	if (found):
		key = 'lhs'
		key2 = 'data'

		ind1 = 1;
		ind2 = 1;

		for element in failed_out['trace']:
			if ('stepType' in element) and (element['stepType'] == 'output'):
					
					data = [val['data'] for val in element['values']]
					if(start_state==0):
						start_state = int(data[0])
						# print(start_state)
						continue

					if(data and data[0] != '0'):
						temp = [ind1,ind2,int(data[0])]
						t.append(temp)
						ind2 = ind2 + 1
					elif (data and data[0] == '0'):
						ind2 = ind2 + 1
			if(ind2 == len(input_dict['event_uniq'])+1):
				ind1 = ind1+1
				ind2 = 1

	f.close()
	return (found,t,start_state)

def get_ce(trace_input):

	event_id = trace_input['event_id']
	event_uniq = trace_input['event_uniq']

	len_ce = l

	seq_input = [];
	for i in range(len(event_id)-len_ce+1):
		# random windows instead of a sliding window
		# ind = random.randint(0,len(events)-3) 
		ind = i
		seq_input.append(event_id[ind:ind+len_ce])

	seq_input_uniq = [list(i) for i in (np.unique(seq_input,axis=0))]
	print(seq_input_uniq)

	b = [list(i) for i in (itertools.product(range(1,len(event_uniq)+1), repeat = len_ce))]

	not_in_seq = [b[i] for i in range(len(b)) if b[i] not in seq_input_uniq]
	#not_in_seq = seq_input_uniq
	found = 1
	if not not_in_seq:
		found = 0

	return (found,not_in_seq)

def plot_model(model,trace_input,start_state):
	# Save generated model as figure: my_state_diagram.png
	
	class vis_trace(object):
		def show_graph(self, **kwargs):
			self.get_graph().draw(trace_filename.replace('.txt','_dfa.png'), prog='dot')
			os.system("mv " + trace_filename.replace('.txt','_dfa.png') + " " + target_model_path)

	event_uniq = trace_input['event_uniq']
	event_id = trace_input['event_id']

	t = np.unique(model,axis=0)
	first_event = [ind for ind in range(len(model)) if model[ind][1] == event_id[0]]
	#start_state = str(model[first_event[0]][0])
	states = []
	for i in range(num_states):
		states.append(str(i+1))

	transitions = []
	for i in range(len(t)):
		temp_trans = [event_uniq[t[i][1]-1],states[t[i][0]-1] ,states[t[i][2]-1]]
		transitions.append(temp_trans)

	print(start_state)
	model = vis_trace()
	machine = GraphMachine(model=model, 
                       states=states, 
                       transitions=transitions,
                       initial = str(start_state),
                       show_auto_transitions=False, # default value is False
                       title="trace_learn",
                       show_conditions=True)
	model.show_graph()

def dfa_traverse(model,trace):
	state = 1
	for i in range(len(trace)):
		if(trace[i] == 1):
			state = 1
		found = [x[2] for x in model if x[0] == state and x[1] == trace[i]]
		if not found:
			print("Missing behavior")
			print(trace[0:i+1])
			return (0,trace[0:i+1])
		else:
			state = found[0]

	return (1,[])




start_time = time.time()

trace_filename = sys.argv[1]
num_states = int(sys.argv[2])
len_seq = int(sys.argv[3])
l = int(sys.argv[4])
target_model_path = sys.argv[5]

incr = 0
change = 0
no_change = 0

C_gen_model = './auxiliary_files/gen_model.c'
C_gen_model_output = './auxiliary_files/cbmc_output_gen_model.json'

input_dict = text_preprocess()

ce_global = []
found_ce = 0

print("Checking model against traces")
(found_ce,ce_global) = get_ce(input_dict)
	
if found_ce:
	print("CE found :")
	print(list(ce_global))
else:
	print("No CE found, generating new model")

if not ce_global:
	print("Model:")
	print(temp_model)
else:
	while(True):
		failed_out = []
		found_model = 0
		final_model = 1
		gen_c_model(input_dict,ce_global,num_states)
		print("Running CBMC...............")
		os.system("cbmc " + C_gen_model + " --trace --json-ui > " + C_gen_model_output)

		(found_model,temp_model,start_state) = get_model()

		if found_model:
			print("Generated model")
			print(temp_model)

			if(final_model):
				print("Final Generated model")
				print(temp_model)
				final_model_gen = temp_model
				break;
		else:
			num_states = num_states + 1
			print("No model, increasing number of states to %d" %(num_states))


##Display model
plot_model(final_model_gen,input_dict,start_state)


# Verifying

print("\n\n\n------------- Verifying: ----------------------------")

while(True):
	(f,beh) = dfa_traverse(final_model_gen,input_dict['event_id'])
	if (f):
		print("All behaviors present\n")
		print("Number of states: " + str(num_states))
		break
	else:
		init_model = final_model_gen
		incr = 1
		o_num_states = num_states
		input_dict['seq_input_uniq'] = [beh]

		while(True):
			failed_out = []
			found_model = 0
			final_model = 1
			if change:
				num_states = o_num_states
			gen_c_model(input_dict,ce_global,num_states)
			print("Running CBMC...............")
			os.system("cbmc " + C_gen_model + " --trace --json-ui > " + C_gen_model_output)

			(found_model,temp_model,start_state) = get_model()

			if found_model:
				print("Generated model")
				print(temp_model)

				if(final_model):
					print("Final Generated model")
					print(temp_model)
					final_model_gen = temp_model
					break;
			else:
				if((num_states > o_num_states) and (num_states - o_num_states) % 5 == 0):
					print("No model, exceeded #states, changing existing transition")
					change = 1
					no_change = 1
					continue
				num_states = num_states + 1
				print("No model, increasing number of states to %d" %(num_states))

##Display model
plot_model(final_model_gen,input_dict,start_state)

end_time = time.time()
print("Time taken: " )
print(end_time-start_time)

