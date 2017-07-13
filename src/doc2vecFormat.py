#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# Run doc2vecFormat.py to combine all walks into one doc2vecFormat.txt file.
# All walks for the corresponding network are ranking by their network name.
# For instance, 1.walks, 2.walks, ..., 110.walks. 
# *********************************************************************

# import the modules needed to run the script
import os

if not os.path.exists('./../data/doc2vec/'):
	os.makedirs('./../data/doc2vec/')

fl = os.listdir('./../data/randomWalks/')
with open('./../data/doc2vec/' + 'doc2vecFormat.txt', 'w') as fo:	
	fwalks = []
	for f in fl:
		if f.endswith('.walks'):
			# print f
			fwalks.append(int(f.strip().replace('.walks', '')))
	fwalks = sorted(fwalks)  # sort file names in asecending order (1.walks, 2.walks, ..., 230.walks)
	# print fwalks

	for f in fwalks:
		with open('./../data/randomWalks/' + str(f)+'.walks', 'r') as fi:
			ls = fi.readlines()
			for l in ls:
				fo.write(l+'\n')

		
			fi.close()
	fo.close()

		


# print 'Done.'