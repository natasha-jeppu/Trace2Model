import sys
import os
from os import listdir
from os.path import isfile, join
import time

from os.path import abspath
from termcolor import colored
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    required_parse = parser.add_argument_group('required arguments')
    required_parse.add_argument('-gen_o','--gen_option', metavar = 'MODEL_GEN_OPTION', required = True, choices=['incr','dfa'],
            help='Automata learning option : incr (incremental), dfa')
    parser.add_argument('-syn', '--syn_type', metavar = 'SYNTHESIS_TYPE', choices=['guard','update',''], default='',
            help='Predicate synthesis: guard, update')

    hyperparams = parser.parse_args()
    return hyperparams

def main():
	hyperparams = parse_args()

	gen_option = hyperparams.gen_option
	syn = hyperparams.syn_type

	file = ''
	file_syn = ''

	if(gen_option == 'dfa'):
		mypath = full_path + 'benchmarks/old_bench/'
		file = full_path + 'dfa.py'
	elif(gen_option == 'incr'):
		mypath = full_path + 'benchmarks/shahar_bench/'
		file = full_path + 'incr.py -o stb'

	if(syn != ''):
		if(syn == 'guard'):
			os.system('python3 ' + full_path + 'syn_next_event.py -i ' + full_path + 'benchmarks/syn_bench/minePump.txt -dv [all] methane:N pump:S')
		elif(syn == 'update'):
			os.system('python3 ' + full_path + 'syn_event_update.py -i ' + full_path + 'benchmarks/syn_bench/uart.txt -v x:N')
			os.system('python3 ' + full_path + 'syn_event_update.py -i ' + full_path + 'benchmarks/syn_bench/integrator_trace.txt -v op:N')
		

	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != '.DS_Store']

	result = []

	if(syn == ''):
		for f in onlyfiles:
			if(f in ['linux.txt','java.net.DatagramSocket.txt','java.net.Socket.txt','attach_device.txt']):
				continue
			print("\nRunning example: " + f)

			start_time = time.time()
			os.system("python3 " + file + " -i " + mypath + f)
			end_time = time.time()

			temp = [f,end_time-start_time]
			result.append(temp)
			print("\n\n")

		for x in result:
			print(x[0] + ': ' + str(x[1]))

	else:
		if(syn == 'guard'):
			start_time = time.time()
			os.system("python3 " + file + " -i " + full_path + "benchmarks/syn_bench/minePump_events.txt")
			end_time = time.time()
			print("Time taken: " + str(end_time-start_time))
		else:
			start_time = time.time()
			os.system("python3 " + file + " -i " + full_path + "benchmarks/syn_bench/uart_events.txt")
			end_time = time.time()
			print("Time taken: " + str(end_time-start_time))
			start_time = time.time()
			os.system("python3 " + file + " -i " + full_path + "benchmarks/syn_bench/integrator_trace_events.txt ")
			end_time = time.time()
			print("Time taken: " + str(end_time-start_time))

full_path = abspath(__file__).replace('run.py','')

if __name__ == '__main__':
	start_time = time.time()
	main()
	end_time = time.time()
	print('\n\nTime taken: ' + str(end_time - start_time))





