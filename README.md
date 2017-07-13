PathEmb 1.0 Python package - Linux version
------------------------

PathEmb 1.0 is a Python package.

This package includes PathEmb 1.0 Python package and related scripts and files for the following paper:

PathEmb: Random Walk based Document Embedding for Global Pathway Similarity Search
(Jiao Zhang, Sam Kwong, and Ka-Chun Wong)


CONTAINS:
------------------------

* src : a folder contains PathEmb 1.0 Python package related scripts and binaries. It has following files :

	* PathEmb.py : PathEmb 1.0 Python module

	* runNetal.sh : shell scripts to run NETAL
	
	* runNetal.py : Python script to run NETAL and get label raw data
	
	* netalEC.py : Python script to extract NETAL EC label
	
	* netalLCCS.py : Python script to extract NETAL LCCS label
	
	* NETAL : NETAL executable binary
	
	* runHubalign.sh : shell script to run HubAlign
	
	* runHubalign.py : Python script to run HubAlign and get label raw data
	
	* hubalignEC.py : Python script to extract HubAlign EC label
	
	* hubalignLCCS.py : Python script to extract HubAlign LCCS label
	
	* HubAlign : HubAlign executable binary

	* randomWalk.py : Python script to get random walks for each vertex	

	* node2vec.py : Python script of node2vec algorithm

	* doc2vecFormat.py : Python script to combine all walks into one file

	* doc2vecTrain.py : Python script to train a doc2vec model

	* doc2vecInfer.py : Python script to infer the feature representation for each pathway

	* csvFea.py : Python script to get feature file

	* csvFeaLab.py : Python script to generate a csv file, which contains final feature and label

	* ABRegression.py : Python script to call AdaBoost regression, train the model and perform pathway query
	
* data : this folder stores all the data related to PathEmb 1.0 Python package. It has following files :

	* rawData : it stores the input pathway txt files of PathEmb 1.0 Python package, which exists in the initial stage
	
	* netalLabel : it stores label files of NETAL, which is created in the program execution stage

	* hubLabel : it stores label files of HubAlign, which is created in the program execution stage

	* randomWalks :  it stores all random walks for each pathway, which is created in the program execution stage

	* doc2vec : it stores all document embedding files, which is created in the program execution stage
	
	* csv : it stores the final csv file (feature and label), which is created in the program execution stage
	
	* output : it stores top k percent similar pathways, which is created in the program execution stage

* LICENSE : MIT License

* README.md : this file


PREREQUISITE
------------------------

PathEmb 1.0 Python package was tested by using Python 2.7.6 version on Ubuntu 14.04 LTS. Following Python packages should be installed:

* scipy

* numpy

* pandas

* scikit-learn

* networkx

* gensim


HOW TO USE
------------------------

* import PathEmb 1.0 Python package
	
	$ cd /PathEmb/src
	
	$ chmod +x *
	
	$ python

	$ import PathEmb

* call functions in PathEmb 1.0 Python package:

	$ PathEmb.helpInfo()

	$ PathEmb.labelExtract(label, dbStart, dbEnd, qStart, qEnd)

	$ PathEmb.randomWalk(r, l, h)

	$ PathEmb.doc2vec(u, d)

	$ PathEmb.csv(label, d, dbStart, dbEnd, qStart, qEnd)

	$ PathEmb.ABRegression(label, K)
 
* Examples:

	$ cd /PathEmb/src
	
	$ chmod +x *

	$ import PathEmb

	$ PathEmb.helpInfo()

	$ PathEmb.labelExtract('m1', 1, 100, 101, 110)

	$ PathEmb.randomWalk(5, 30, 1)

	$ PathEmb.doc2vec(15, 50)

	$ PathEmb.csv('m1', 50, 1, 100, 101, 110)

	$ PathEmb.ABRegression('m1', 10)

* Parameters:

	* [label] : m1, m2, m3 or m4 (m1: NETAL EC, m2: NETAL LCCS, m3: HubAlign EC, m4: HubAlign LCCS)

	* [dbStart] : integer number, it should be the smallest file name in the database

	* [dbEnd] : integer number, it should be the largest file name in the database

	* [qStart] : integer number, it should be the smallest file name in the query pathway set

	* [qEnd] : integer number, it should be the largest file name in the query pathway set

	* [r] : integer number, it is the random walks per vertex

	* [l] : integer number, it is the walk length

	* [h] : integer number, it is the direction guidance of walk

	* [u] : integer number, it is the window size

	* [d] : integer number, it is the feature dimension

	* [K] : integer number, it is the top K percent


FILE NAMING RULE
------------------------

* Input pathway file is named in the txt file format. File name is interger number. File name in the database should not have any interaction with the query set file name.

* For example, if there are 100 pathways in the database and 10 query pathways in the query set. Therefore, file names in the database should start from 1.txt to 100.txt. File names in the query set should start from 101.txt to 110.txt.


FILE FORMAT OF PATHEMB
------------------------

* Input pathway is in the txt file format, which has the following format: 

 Each line corresponds to an interaction and contains the name of two nodes and the edge weight of the corresponding interaction (separated by a tab). The nodes can be presented by integer or string.

 Here is an example for pathway "1.txt" :

	1	2	1

	1	3	2.3

	2	3	5.7

	3	4	1

	1	4	9.4

* Output file is in the csv file format, which has the following format: 

 The output file returns top K similar pathways against each query pathway. Each line contains the name of the query pathway, the name of similar netowrk in the database, label for regression and prediction of the similarity score (separated by a comma).

 Here is an example for the output file "topkpathway.csv" :

	q_name	db_name	label	predictions

	101	45	0.7	0.4

	101	28	0.6	0.9

	101	64	0.7	0.8

	101	95	0.5	0.6

	101	38	0.2	0.3


FUNDING SUPPORT
------------------------
* We would like to thank Amazon Web Service (AWS) for providing cloud credits for the software development.


------------------------
Jiao Zhang

jiaozhang9-c@my.cityu.edu.hk

July 13 2017

