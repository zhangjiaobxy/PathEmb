#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# ABR: adaboost regression  (# http://scikit-learn.org/stable/auto_examples/ensemble/plot_adaboost_regression.html)
# read csv file (including feature and label) and use ABR to get the top k similar 
# pathways for each query pathway
# *********************************************************************

# import the modules needed to run the script
from __future__ import division
from sklearn.ensemble import AdaBoostRegressor  
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import pandas as pd
import os,sys,time,math,subprocess,shutil

metricLabel = str(sys.argv[1])
topk = int(sys.argv[2])  # top k similar pathways

if metricLabel == 'm1':
    print 'You have selected \''+metricLabel+': NETAL EC\' as your label.\n'
    label_file = 'netal_ec_label.txt'
elif metricLabel == 'm2':
    print 'You have selected \''+metricLabel+': NETAL LCCS\' as your label.\n'
    label_file = 'netal_lccs_label.txt'
elif metricLabel == 'm3':
    print 'You have selected \''+metricLabel+': HubAlign EC\' as your label.\n'
    label_file = 'hubalign_ec_label.txt'
elif metricLabel == 'm4':
    print 'You have selected \''+metricLabel+': HubAlign LCCS\' as your label.\n'
    label_file = 'hubalign_lccs_label.txt'
else:
    print 'Invalid label, system exit!'
    print '\n*********************************************************************\n'
    raise SystemExit 

print 'csv file name: ', 'csvFea_'+label_file.strip().replace('.txt', '.csv'), '\n'

########################## clean data ##################################################
df = pd.read_csv('./../data/csv/csvFea_'+label_file.strip().replace('.txt', '.csv'), skipinitialspace=True, delimiter=',')
df = df.fillna(0)  # replace NaN with 0
df = df.loc[(df.sum(axis=1) != 0), (df.sum(axis=0) != 0)]  # remove 0 columns and rows


########################## initialization ##################################################
k = 10  # 10-fold cross-validation
n = df.shape[0]/k  # size of each fold
inc = 0
feature = df.columns[2:(df.shape[1]-1)]  # feature column names
label = df.columns[df.shape[1]-1]  # label column name
db_size = len(df.db_name.unique())  # database size
q_size = len(df.q_name.unique())  # the number of query networks
train_time_s = []
test_time_s = []
out_df_topk = pd.DataFrame()  # top k similar networks against each query network
out_df_save = pd.DataFrame()  # all the networks


########################## k-fold cross-validation ##########################################
for i in range(0,k):
	s1 = int(i * n)
	s2 = int((i+1) * n)
	test = df[s1:s2]  # test data
	train = (df[:s1]).append(df[s2:])  # train data

	########################## model: train / test ###############################################
	# train
	train_start = float(round(time.time() * 1000))  # millisecond
	dtr = DecisionTreeRegressor(max_features='sqrt', random_state=23, max_depth= None)
	abr = AdaBoostRegressor(base_estimator = dtr, n_estimators=100)
	abr.fit(train[feature], train[label])
	train_end = float(round(time.time() * 1000))
	train_time = train_end - train_start
	train_time_s.append(train_time)

	# test
	test_start = float(round(time.time() * 1000))
	abr_prediction = abr.predict(test[feature])
	test_end = float(round(time.time() * 1000))
	test_time = test_end - test_start
	test_time_s.append(test_time)

	predictions = pd.DataFrame(abr_prediction, columns=['predictions'])  # prediction column
	q_db_df = pd.concat([test['q_name'],test['db_name'],test[label]],axis=1).reset_index()  # q_name, db_name, and label dataframe
	out_df = (pd.concat([q_db_df, predictions],axis=1))  # q_name, db_name, label, and prediction dataframe
	out_df_save = out_df_save.append(out_df)


########################## avg time cost ##########################################
avg_train_time = np.mean(train_time_s)  # average training time for each fold (millisecond)
avg_test_time = (np.mean(test_time_s))/(q_size/k)  # average query time for each query network


######################### output / write to file ####################################################
if not os.path.exists('./../data/output/'):  # the topk networks
    os.makedirs('./../data/output/')
if not os.path.exists('./../data/output/allResult/'):  # all the networks
    os.makedirs('./../data/output/allResult/')

# save topk predictions
topk_perc = int(math.ceil(topk/100 * db_size))  # the number of the topk networks
q_test_size = len(out_df_save.q_name.unique())  # the number of query networks 
for q in range(0,q_test_size):  # get top k similar networks against each query network
	out_df_e = (out_df_save[inc:inc+db_size]).sort_values(['predictions'],ascending=False)[:topk_perc]
	inc = inc + db_size
	out_df_topk = out_df_topk.append(out_df_e)
out_df_topk = out_df_topk.sort_values(['q_name'],ascending=True)
out_df_topk.to_csv('./../data/output/csvFea_'+label_file.strip().replace('.txt','_top'+str(topk)+'%.csv') , header=True, cols=['q_name','db_name',label,'predictions'], index = False)  # top k similar network output file

########################## simpson overlap ##########################################
# save all predictions
out_df_save = out_df_save.sort_values(['q_name'],ascending=True)
out_df_save.to_csv('./../data/output/allResult/'+label_file.strip().replace('.txt','.csv'), header=True, cols=['q_name','db_name',label,'predictions'], index = False)

ol_f = open('./../data/output/allResult/'+label_file.strip().replace('.txt','.csv'), 'r')
ols = ol_f.readlines()[1:]
qname_set = set()
for ol in ols:
	qname = ol.strip().split(',')[0]
	qname_set.add(float(qname))  # all the query network name
ol_values = []
for e_qname in qname_set:
	block = []  # all db network related to each of the query network
	for ol in ols:
		if float(ol.strip().split(',')[0]) == e_qname:
			block.append(ol)

	block_label = sorted(block,key=lambda x:float(x.strip().split(',')[2]), reverse=True)  # sort each query block by the label column
	block_pred = sorted(block,key=lambda x:float(x.strip().split(',')[3]), reverse=True)  # sort each query block by the prediction column

	db_labels = []  # db names column by sorting labels in descending order
	db_preds = []  # db names column by sorting predictions in descending order
	for e_block_label in block_label:
		db_label = e_block_label.strip().split(',')[1]
		db_labels.append(db_label)
	db_labels_topk=db_labels[:topk_perc]
	for e_block_pred in block_pred:
		db_pred = e_block_pred.strip().split(',')[1]
		db_preds.append(db_pred)
	db_preds_topk=db_preds[:topk_perc]
	ol_value = len(set(db_labels_topk).intersection(db_preds_topk))/topk_perc
	ol_values.append(ol_value)
ol = round(np.mean(ol_values),5)  # save 5 digit number

if os.path.exists('./../data/output/allResult/'):  # remove the dir and its files
    shutil.rmtree('./../data/output/allResult/')


print '*********************************************************************\n'	
print 'The output file is: ', 'csvFea_'+label_file.strip().replace('.txt','_top'+str(topk)+'%.csv'), '\n'
print 'Simpson overlap coefficient is: ', ol, '\n'
print 'Average training time for',k,'fold cross validation is',avg_train_time, 'msec.\n'
print 'Average testing time for',k,'fold cross validation is',avg_test_time, 'msec.\n'
print '\n*********************************************************************\n'
