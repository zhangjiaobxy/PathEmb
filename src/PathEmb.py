# PathEmb package
import os, sys, subprocess, argparse

########################################################################
# step 0: 
#		print help info of PathEmb
# callExample: 
#		PathEmb.helpInfo()

def helpInfo():
	parser = argparse.ArgumentParser(description = 'Run PathEmb.')
	parser.add_argument('label', nargs = '?', default = 'm1', help = 'Label of regression. m1: NETAL EC, m2: NETAL LCCS, m3: HubAlign EC, m4: HubAlign LCCS')
	parser.add_argument('dbStart', nargs = '?', default = 1, help = 'Start number of DB. Default is 1.')
	parser.add_argument('dbEnd', nargs = '?', default = 100, help = 'End number of DB. Default is 100.')
	parser.add_argument('qStart', nargs = '?', default = 101, help = 'Start number of query set. Default is 101.')
	parser.add_argument('qEnd', nargs = '?', default = 110, help = 'End number of query set. Default is 110.')
	parser.add_argument('r', nargs = '?', default = 5, help = 'Random walks per vertex. Default is 5.')
	parser.add_argument('l', nargs = '?', default = 30, help = 'Walk length. Default is 30.')
	parser.add_argument('h', nargs = '?', default = 1, help = 'Direction guidance of walk. Default is 1.')
	parser.add_argument('u', nargs = '?', default = 15, help = 'Window size. Default is 15.')
	parser.add_argument('d', nargs = '?', default = 50, help = 'Feature dimension. Default is 50.')
	parser.add_argument('K', nargs = '?', default = 10, help = 'Top K percent similar pathways. Default is 10.')
	parser.print_help()
	print '\nusage: call functions of PathEmb: '
	print '  0. get help info:'
	print '    PathEmb.helpInfo()'
	print '  1. get label file:'
	print '    PathEmb.labelExtract(label, dbStart, dbEnd, qStart, qEnd)'
	print '    PathEmb.labelExtract(\'m1\', 1, 100, 101, 110)'
	print '  2. get random walks for each vertex:'
	print '    PathEmb.randomWalk(r, l, h)'
	print '    PathEmb.randomWalk(5, 30, 1)'
	print '  3. get feature representation of pathway:'
	print '    PathEmb.doc2vec(u, d)'
	print '    PathEmb.doc2vec(15, 50)'
	print '  4. get csv file of the AdaBoost regression:'
	print '    PathEmb.csv(label, d, dbStart, dbEnd, qStart, qEnd)'
	print '    PathEmb.csv(\'m1\', 50, 1, 100, 101, 110)'
	print '  5. run AdaBoost regression:'
	print '    PathEmb.ABRegression(label, K)'
	print '    PathEmb.ABRegression(\'m1\', 10)'


########################################################################
# step 1: 
#		run labelExtract to get label files
# input: 
#		./data/rawData/
# output: 
#		./data/netalLabel (netal output file: netal_ec_label.txt, netal_lccs_label.txt)
#       ./data/hubLabel (hubalign output file: hubalign_ec_label.txt, hubalign_lccs_label.txt)
# parameter: 
#       label (label = m1, m2, m3, m4)
#             (m1: NETAL EC, m2: NETAL LCCS, m3: HubAlign EC, m4: HubAlign LCCS)
#       dbStart: the start range of database
#       dbEnd: the end range of database
#       queryStart: the start range of query networks
#       queryEnd: the end range of query networks
# callExample: 
#		PathEmb.labelExtract('m1', 1, 100, 101, 110)

def labelExtract(label, dbStart, dbEnd, queryStart, queryEnd):
    if label == 'm1' or label == 'm2':
        os.system('bash runNetal.sh ' + str(dbStart) + ' ' + str(dbEnd) + ' ' + str(queryStart) + ' ' + str(queryEnd))
    elif label == 'm3' or label == 'm4':
        os.system('bash runHubalign.sh ' + str(dbStart) + ' ' + str(dbEnd) + ' ' + str(queryStart) + ' ' + str(queryEnd))
    else:
        print '\n*********************************************************************\n'
        print "Invalid label, system exit! "
        print '\n*********************************************************************\n'
        raise SystemExit

########################################################################
# step 2: 
#		run randomWalk.py to get random walks for each vertex
# input: 
# 		./data/rawData/ (*.txt file)
# output: 
#		./data/randomWalks/ (*.walks file)
# parameter: 
# 		r: random walks per vertex
# 		l: walk length
# 		h: direction guidance of walk
# callExample:
#		PathEmb.randomWalk(5,30,1)

def randomWalk(r, l, h):
	cmd = 'python randomWalk.py ' + '--r ' + str(r) + ' --l ' + str(l) + ' --h ' + str(h)
	os.system(cmd)

########################################################################
# step 3: 
#		run doc2vec to get the feature representation of pathway
# input: 
# 		./data/randomWalks/ (*.walks file)
# output: 
#		./doc2vec/doc2vecFormat_train.bin
# 		./doc2vec/doc2vecFormat_infer.txt
# parameter: 
# 		u: window size
# 		d: feature dimension (vector size)
# callExample:
#		PathEmb.doc2vec(15, 50)

def doc2vec(u, d):
	cmd1 = 'python doc2vecFormat.py'
	cmd2 = 'python doc2vecTrain.py ' + str(u) + ' ' + str(d)
	cmd3 = 'python doc2vecInfer.py'
	os.system(cmd1)
	os.system(cmd2)
	os.system(cmd3)

########################################################################
# step 4: 
#		run csv to get the csv file of feature and label
# input: 
# 		./data/doc2vec/doc2vecFormat_infer.txt (feature file)
#		./data/netalLabel (label file of netal: netal_ec_label.txt, netal_lccs_label.txt), or,
#       ./data/hubLabel (label file of hubalign: hubalign_ec_label.txt, hubalign_lccs_label.txt)
# output: 
#		./data/doc2vec/csvFea.csv
# 		./data/csv/csvFea_*label.csv
# parameter: 
#       label (label = m1, m2, m3, m4)
#             (m1: NETAL EC, m2: NETAL LCCS, m3: HubAlign EC, m4: HubAlign LCCS)
# 		d: feature dimension (vector size)
#       dbStart: the start range of database
#       dbEnd: the end range of database
#       queryStart: the start range of query networks
#       queryEnd: the end range of query networks
# callExample:
#		PathEmb.doc2vec('m1', 50, 1, 100, 101, 110)

def csv(label, d, dbStart, dbEnd, queryStart, queryEnd):
	cmd1 = 'python csvFea.py ' + str(dbStart) + ' ' + str(dbEnd) + ' ' + str(queryStart) + ' ' + str(queryEnd)
	cmd2 = 'python csvFeaLab.py ' + str(d) + ' ' + str(label)
	os.system(cmd1)
	os.system(cmd2)

########################################################################
# step 5: 
# 		run AdaBoost regression
# input: 
# 		./data/csv/csvFea_*label.csv
# output: 
# 		./data/output/csvFea_*label_topK%.csv
# parameter: 
#		label (label = m1, m2, m3, m4)
#			  (m1: NETAL EC, m2: NETAL LCCS, m3: HubAlign EC, m4: HubAlign LCCS)
#		K (output top K percent similar pathways)
# callExample: PathEmb.ABRegression('m1', 10)

def ABRegression(label, K):
    cmd = 'python ABRegression.py ' + str(label) + ' ' + str(K)
    os.system(cmd)

########################################################################
