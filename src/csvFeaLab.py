#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# Run csvFeaLab.py to get the final csv file as the input of regression algorithm
# *********************************************************************

# import the modules needed to run the script
import os, sys, subprocess
import pandas as pd

d = int(sys.argv[1])  # feature dimension (vector size)
metricLabel = sys.argv[2]

if metricLabel == 'm1':
    print 'You have selected \''+metricLabel+': NETAL EC\' as your label.'
    label_file = 'netal_ec_label.txt'
    flabel=open('./../data/netalLabel/'+label_file,'r')
elif metricLabel == 'm2':
    print 'You have selected \''+metricLabel+': NETAL LCCS\' as your label.'
    label_file = 'netal_lccs_label.txt'
    flabel=open('./../data/netalLabel/'+label_file,'r')
elif metricLabel == 'm3':
    print 'You have selected \''+metricLabel+': HubAlign EC\' as your label.'
    label_file = 'hubalign_ec_label.txt'
    flabel=open('./../data/hubLabel/'+label_file,'r')
elif metricLabel == 'm4':
    print 'You have selected \''+metricLabel+': HubAlign LCCS\' as your label.'
    label_file = 'hubalign_lccs_label.txt'
    flabel=open('./../data/hubLabel/'+label_file,'r')
else:
    print 'Invalid label, system exit!'
    print '\n*********************************************************************\n'
    raise SystemExit

# para:
# dim = 50
# na_label = 'ec_netal'  (or label = 'lccs_netal')
# db_size = 200 (database size, for aids=500, bos=200, homo=260, mus=90)


# import os


# dim = 150
# na_label = 'lccs_hubalign'

if not os.path.exists('./../data/csv/'):
	os.makedirs('./../data/csv/')

# db_size = 200
# dimList = [50]
# dim =50
# na_label_list = ['ec_netal','lccs_netal','ec_hubalign','lccs_hubalign']
# na_label = 'netal_ec_label'
# for dim in dimList:
# for na_label in na_label_list:


# flabel = open('./../data/netalLabel/' + na_label + '.txt', 'r')
# ffeature = open('./../2_csvFormat/csvFormat_dim'+str(dim)+'.csv', 'r')

# handle label
lslabel = flabel.readlines()
llabel_list = []
for llabel in lslabel:
	llabel = llabel.strip().replace('.txt', '')
	llabel_list.append(llabel)
# print llabel_list[:10]
# print len(llabel_list)
llabel_list = sorted(llabel_list, key = lambda x:float(x.strip().split('\t')[1]))
llabel_list = sorted(llabel_list, key = lambda x:float(x.strip().split('\t')[0]))
# print llabel_list[0:210]
label_column = []
for item in llabel_list:
	item = item.strip().split('\t')[-1]
	label_column.append(item)
# print label_column[0:10]

# handle feature
df = pd.read_csv('./../data/doc2vec/csvFea.csv', header = None, delimiter='\t')
label = pd.DataFrame(label_column)
csvFinal = pd.concat([df,label],axis = 1)
# csvFinal.to_csv('csvFinal_ecdim100.csv', header = False, index = False)
csvFinal.to_csv('./../data/csv/' + 'csvFea_'+label_file.strip().replace('.txt', '')+'_mid.csv', header = False, index = False)

flabel.close()


# ffeature.close()
csvFinal = open('./../data/csv/' + 'csvFea_'+label_file.strip().replace('.txt', '')+'_mid.csv', 'r')
csvFeaLab = open('./../data/csv/' + 'csvFea_'+label_file.strip().replace('.txt', '')+'.csv', 'w')

# firstL = 'q_name,db_name,q1,q2,q3,q4,47,db48,db49,db50,'+na_label+'\n'
# print type(firstL)

# the header of csv file
xq_s = ''  # q string
xdb_s = ''  # db string
for x in range(d):
	xq =  'q'+str(x+1)
	xq_s = xq_s + ',' + xq
	xdb = 'db'+str(x+1)
	xdb_s = xdb_s + ',' + xdb
# print xq_s
# print xdb_s
# print type(xq_s)
# print type(xdb_s)
firstL = 'q_name,db_name' + xq_s + xdb_s + ',' + label_file.strip().replace('.txt', '') + '\n'
# print firstL


csvFeaLab.write(firstL)
lsFL = csvFinal.readlines()
for lFL in lsFL:
	csvFeaLab.write(lFL)
csvFeaLab.close()

if os.path.exists('./../data/csv/' + 'csvFea_'+label_file.strip().replace('.txt', '')+'_mid.csv'):
	os.remove('./../data/csv/' + 'csvFea_'+label_file.strip().replace('.txt', '')+'_mid.csv')


# print 'Done.'




























