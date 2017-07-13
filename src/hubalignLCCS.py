#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# extract hubalign lccs label
# *********************************************************************

# import the modules needed to run the script
import os, sys

# db range
dbStart = int(sys.argv[1])
dbEnd = int(sys.argv[2]) 

f_n = []
lccs = []
lccs_store = []
file_list = os.listdir('.')
for file_name in file_list:
	if file_name.endswith('.eval'):
		if dbStart <= float(file_name.replace('.txt.eval','').split('-')[-1]) <= dbEnd:
			f_n.append(file_name)

for each_name in f_n:
	f_original = open(each_name,'r')
	each_line = f_original.readline()
	for each_line in f_original:
		if 'Edges =' in each_line:
			lccs = each_line.strip().split(' ')[-1]
			lccs_store.append(lccs)

f_generate = open('hubalign_lccs_label' + '.txt', 'w')

i = 0
final_f_s = []
final_f_first = ''
final_f_second = ''
for i in range(len(lccs_store)):
	if i < len(lccs_store):
		final_f_first = f_n[i].replace('.eval','').replace('.txt','').strip().split('-')[0]
		final_f_second = f_n[i].replace('.eval','').replace('.txt','').strip().split('-')[1]
		final_f =  final_f_first + '\t' + final_f_second + '\t' + lccs_store[i] +'\n'
		final_f_s.append(final_f)
		i = i + 1
		continue

final_f_s = sorted(final_f_s, key=lambda x:float(x.split('\t')[1]))
final_f_s = sorted(final_f_s, key=lambda x:float(x.split('\t')[0]))

for e in final_f_s:
	espl = e.strip().split('\t')
	qname = str(espl[0]) + '.txt'
	dbname = str(espl[1]) + '.txt'
	label = str(espl[2])
	f_generate.write(qname + '\t' +dbname + '\t' + label + '\n')

print '\n*********************************************************************\n'
print 'Congratulation! Label file is generated successfully!'
print '\n*********************************************************************\n'