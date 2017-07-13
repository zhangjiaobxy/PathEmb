#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# Run csvFea.py to get features files for q and db
# *********************************************************************

# import the modules needed to run the script
import os, sys, subprocess

dbStart = int(sys.argv[1])
dbEnd = int(sys.argv[2])
queryStart = int(sys.argv[3])
queryEnd = int(sys.argv[4])


# dbStart = 1
# dbEnd = 100
# queryStart = 101
# queryEnd = 110
# dim = 50
# dimList = [50]
# for dim in dimList:
# get the db and q feature file seperately
ficsv = open('./../data/doc2vec/doc2vecFormat_infer.txt', 'r')
fdb = open('./../data/doc2vec/doc2vecFormat_infer_db.txt', 'w')
fq = open('./../data/doc2vec/doc2vecFormat_infer_q.txt', 'w')
ls = ficsv.readlines()
for ldb in ls[dbStart-1 : dbEnd]:
	fdb.write(ldb)
for lq in ls[queryStart-1 : queryEnd]:
	fq.write(lq)
fdb.close()
fq.close()

focsv = open('./../data/doc2vec/csvFea.csv', 'w')  # file format is: qname dbname q_dim_1...q_dim_n db_dim_1...db_dim_x

fdb = open('./../data/doc2vec/doc2vecFormat_infer_db.txt', 'r')
fq = open('./../data/doc2vec/doc2vecFormat_infer_q.txt', 'r')
lsdb = fdb.readlines()
lsq = fq.readlines()
sdb = len(lsdb)
sq = len(lsq)
# print sdb
# print sq

qnum = sdb  # number of query networks
for lq in lsq:	
	qnum = qnum + 1
	dbnum = 0  # number of db networks
	for ldb in lsdb:
		dbnum = dbnum + 1
		focsv.write(str(qnum) + '\t' + str(dbnum) + '\t' + lq.strip().replace(' ', '\t') + '\t' + ldb.strip().replace(' ', '\t') + '\n')
# print qnum
# print dbnum

focsv.close()
fdb.close()
fq.close()	

if os.path.exists('./../data/doc2vec/doc2vecFormat_infer_db.txt'):
	os.remove('./../data/doc2vec/doc2vecFormat_infer_db.txt')
if os.path.exists('./../data/doc2vec/doc2vecFormat_infer_q.txt'):
	os.remove('./../data/doc2vec/doc2vecFormat_infer_q.txt')		


# print 'Done.'