import sys
import os
from os import listdir
from os.path import isfile, join
import time

# mypath = './benchmarks/old_bench/'
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != '.DS_Store']

# target_model_path = os.getcwd() + '/models/'
# for f in onlyfiles:
# 	print("\nRunning example: " + f)
# 	os.system("python3 trace2model_mod_v7_with_start_state.py " + mypath + f + " 2 3 2 " + target_model_path)
# 	# os.system("python3 merged_v9.py " + mypath + f + " 2 3 " + target_model_path)
# 	print("\n\n")

mypath = './benchmarks/old_bench/'
# mypath = './benchmarks/shahar_bench/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != '.DS_Store']

result = []
target_model_path = ''
for f in onlyfiles:
	print("\nRunning example: " + f)
	start_time = time.time()
	# os.system("python3 incr.py -i " + mypath + f + " -o stb")
	os.system("python3 dfa.py -i " + mypath + f + " -t .")
	end_time = time.time()
	temp = [f,end_time-start_time]
	result.append(temp)
	print("\n\n")

for x in result:
	print(x[0] + ': ' + str(x[1]))