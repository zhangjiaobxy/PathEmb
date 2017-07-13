#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# run netal to get raw label files
# *********************************************************************

# import the modules needed to run the script
import os, sys, subprocess

# list all raw data files
file_list = os.listdir(".")

# db range
dbStart = int(sys.argv[1])
dbEnd = int(sys.argv[2]) 
# query range
queryStart = int(sys.argv[3])
queryEnd = int(sys.argv[4])

# number of parrallel subprocess 
thread_num = 8
thread_list = []

# netal commond line
cmd_temp = "./NETAL [FILENAME_2] [FILENAME_1] -i 1"

file_list_1 = []  # db network file list
file_list_2 = []  # query network file list
for e_file in file_list:
    if e_file.endswith('.txt'):
        if e_file.endswith('Details.txt'):
            continue
        if e_file.endswith('Log.txt'):
            continue
        if dbStart <= float(e_file.replace('.txt','')) <= dbEnd:
	        file_list_1.append(e_file)
        elif queryStart <= float(e_file.replace('.txt','')) <= queryEnd:
            file_list_2.append(e_file)

if len(thread_list) < thread_num:
    for e_file_2 in file_list_2:
        for e_file_1 in file_list_1:
            cmd = cmd_temp.replace("[FILENAME_2]", e_file_2).replace("[FILENAME_1]", e_file_1)
            thread = subprocess.Popen(cmd, shell=True)
            thread_list.append(thread)
else:
    for thread in thread_list:
        thread.poll()
        if thread.returncode != None:
            thread_list.remove(thread)
            break

for thread in thread_list:
    thread.communicate()
