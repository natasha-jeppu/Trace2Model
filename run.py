import sys
import os
from os import listdir
from os.path import isfile, join

# mypath = './benchmarks/old_bench/'
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != '.DS_Store']

# target_model_path = os.getcwd() + '/models/'
# for f in onlyfiles:
# 	print("\nRunning example: " + f)
# 	os.system("python3 trace2model_mod_v7_with_start_state.py " + mypath + f + " 2 3 2 " + target_model_path)
# 	# os.system("python3 merged_v9.py " + mypath + f + " 2 3 " + target_model_path)
# 	print("\n\n")

mypath = './benchmarks/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != '.DS_Store']

target_model_path = os.getcwd() + '/models/'
for f in onlyfiles:
	print("\nRunning example: " + f)
	os.system("python3 merged_v9.py " + mypath + f + " 2 3 " + target_model_path)
	print("\n\n")